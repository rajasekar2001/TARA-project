from rest_framework import serializers
from .models import BusinessPartner, BusinessPartnerKYC,fetch_ifsc_code
import re
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

def validate_pan_number(value):
    """
    Validate if the given value is a valid PAN number.
    """
    pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    if not re.match(pan_pattern, value):
        raise serializers.ValidationError("Invalid PAN number format. Expected: ABCDE1234F")
    return value

def validate_gst_number(value):
    """
    Validates if the given value is a valid GSTIN (India).
    Format: 2-digit state code + 10-character PAN + 1 entity code + 'Z' + 1 checksum character.
    Example: 22AAAAA1234A1Z5
    """
    gst_pattern = r'^[0-3][0-9][A-Z]{5}[0-9]{4}[A-Z][0-9A-Z]Z[0-9A-Z]$'
    if not re.match(gst_pattern, value):
        raise serializers.ValidationError(f"'{value}' is not a valid GST number. Expected format: 22AAAAA1234A1Z5.")
    return value

def validate_aadhar_no(value):
    if not re.match(r'^[0-9]{12}$', value):
        raise serializers.ValidationError(_("Invalid Aadhar Number. It must be exactly 12 digits."))
    return value

def validate_ifsc_code(value):
    ifsc_pattern = r'^[A-Z]{4}[0-9]{7}$'
    if not re.match(ifsc_pattern, value):
        raise serializers.ValidationError(_("Invalid IFSC Code. Expected format: ABCD0123456."))
    return value

def validate_mobile_no(value):
    if not value.isdigit():
        raise serializers.ValidationError(_("Mobile number must contain only digits."))
    if not (10 <= len(value) <= 15):
        raise serializers.ValidationError(_("Mobile number must be between 10 to 15 digits."))
    return value
    
# msme number validator
def validate_msme_no(value):
    """Validate MSME (Udyog Aadhaar) number."""
    msme_pattern = r'^[Uu][Dd][Yy]\d{2}[A-Za-z]{3}\d{7}$'
    
    if not re.fullmatch(msme_pattern, value, re.IGNORECASE):
        raise serializers.ValidationError(_("Invalid MSME format. Expected format: UDY12ABC1234567."))

    return value  # Return value if validation passes

class BusinessPartnerKYCSerializer(serializers.ModelSerializer):
    """
    Serializer for BusinessPartnerKYC model with explicit fields and custom validation.
    """
    pan_no = serializers.CharField(validators=[validate_pan_number], required=False, allow_blank=True)
    gst_no = serializers.CharField(validators=[validate_gst_number], required=False, allow_blank=True)
    aadhar_no = serializers.CharField(validators=[validate_aadhar_no], required=False, allow_blank=True)
    ifsc_code = serializers.CharField(validators=[validate_ifsc_code], required=False, allow_blank=True)
    msme_no = serializers.CharField(validators=[validate_msme_no], required=False, allow_blank=True)

    class Meta:
        model = BusinessPartnerKYC
        fields = [
            'bp_code', 'bis_no', 'bis_attachment', 'gst_no', 'gst_attachment', 
            'msme_no', 'msme_attachment', 'pan_no', 'pan_attachment', 
            'tan_no', 'tan_attachment', 'image', 'name', 'aadhar_no', 
            'aadhar_attach', 'bank_name', 'account_name', 'account_no',
            'ifsc_code', 'branch', 'bank_city', 'bank_state', 'note', 'status',
            
        ]

    def create(self, validated_data):
        if not validated_data.get("ifsc_code"):
            bank_name = validated_data.get("bank_name")
            branch = validated_data.get("branch")
            if bank_name and branch:
                fetched_ifsc = fetch_ifsc_code(bank_name, branch)
                if fetched_ifsc:
                    validated_data["ifsc_code"] = fetched_ifsc
                else:
                    raise serializers.ValidationError("Could not fetch IFSC Code. Please enter manually.")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if not validated_data.get("ifsc_code") and instance.bank_name and instance.branch:
            fetched_ifsc = fetch_ifsc_code(instance.bank_name, instance.branch)
            if fetched_ifsc:
                validated_data["ifsc_code"] = fetched_ifsc
        return super().update(instance, validated_data)
class BusinessPartnerSerializer(serializers.ModelSerializer):
    """
    Serializer for BusinessPartner model with explicit fields and nested KYC details.
    """
    kyc_details = BusinessPartnerKYCSerializer(many=True, read_only=True, source='businesspartnerkyc_set')
    mobile = serializers.CharField(validators=[validate_mobile_no])
    alternate_mobile = serializers.CharField(validators=[validate_mobile_no], required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    # class Meta:
    #     model = BusinessPartner
    #     fields = '__all__'
    class Meta:
        model = BusinessPartner
        fields = [
            'bp_code', 'term', 'business_name', 'full_name', 'mobile', 'alternate_mobile',
            'landline', 'alternate_landline', 'email', 'business_email', 'refered_by', 'mobile', 'more', 'door_no', 'shop_no', 'complex_name',
            'building_name', 'street_name', 'area', 'pincode', 'city', 'state', 'map_location', 'location_guide',
            'kyc_details'
        ]
        read_only_fields = ['status'] 
        
        
    def validate(self, data):
        mobile = data.get('mobile')
        instance = self.instance 

        if mobile:
            queryset = BusinessPartner.objects.filter(mobile=mobile)

            # If updating, exclude the current record from the check
            if instance:
                queryset = queryset.exclude(id=instance.id)

            # If another record exists with the same mobile, raise an error
            if queryset.exists():
                raise serializers.ValidationError({"mobile": _("This Mobile Number already exists, Please enter a different Number.")})

        return data

    def create(self, validated_data):
        user = self.context.get('request').user if self.context.get('request') else None
        if user is None or user.role_name not in ["super_admin", "admin", "Project Owner", "Super User"]:
            raise serializers.ValidationError("You do not have permission to create a Business Partner.")
        validated_data['user_id'] = user
        return super().create(validated_data)
    
    
    # def create(self, validated_data):
    #     email = validated_data.get('business_email')
    #     if email and BusinessPartner.objects.filter(business_email=email).exists():
    #         raise ValidationError({"business_email": "A Business Partner with this email already exists."})
        
    #     user = self.context.get('request').user if self.context.get('request') else None
    #     if user is None or user.role_name not in ["super_admin", "admin", "Project Owner", "Super User"]:
    #         raise serializers.ValidationError("You do not have permission to create a Business Partner.")
        
    #     validated_data['user_id'] = user
    #     return super().create(validated_data)
    
    
    
    
    # def create(self, validated_data):
    #     email = validated_data.get('business_email')
    #     if BusinessPartner.objects.filter(business_email=email).exists():
    #         raise ValidationError({"business_email": "A Business Partner with this email already exists."})
    #     return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    
    
class BusinessPartnerKYCSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = BusinessPartnerKYC
        fields = [
            'bp_code', 'bis_no', 'bis_attachment', 'gst_no', 'gst_attachment', 
            'msme_no', 'msme_attachment', 'pan_no', 'pan_attachment', 
            'tan_no', 'tan_attachment', 'image', 'name', 'aadhar_no', 
            'aadhar_attach', 'bank_name', 'account_name', 'account_no',
            'ifsc_code', 'branch', 'bank_city', 'bank_state', 'note', 'status',
            
        ]

    def get_status(self, obj):
        if obj.revoked:
            return 'Revoked'
        if obj.freezed:
            return 'Freezed'
        if all([
    obj.bp_code, obj.bis_no, obj.bis_attachment, obj.gst_no, obj.gst_attachment,
    obj.msme_no, obj.msme_attachment, obj.pan_no, obj.pan_attachment,
    obj.tan_no, obj.tan_attachment, obj.image, obj.name, obj.aadhar_no,
    obj.aadhar_attach, obj.bank_name, obj.account_name, obj.account_no,
    obj.ifsc_code, obj.branch, obj.bank_city, obj.bank_state
]):

           
            return 'Approved'
        return 'Pending'



