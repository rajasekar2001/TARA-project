from rest_framework import serializers
from .models import BusinessPartner, BusinessPartnerKYC,fetch_ifsc_code
import re
from django.utils.translation import gettext_lazy as _

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
            'id', 'bp_code', 'bis_no', 'gst_no', 'msme_no', 'pan_card_image', 'pan_no', 'tan_no', 'aadhar_front_image',
            'aadhar_back_image', 'aadhar_no', 'bank_name', 'account_name', 'account_no',
            'ifsc_code', 'branch', 'bank_city', 'bank_state', 'note'
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

    class Meta:
        model = BusinessPartner
        fields = [
            'id', 'bp_code', 'term', 'business_name', 'name', 'mobile', 'alternate_mobile',
            'landline', 'business_email', 'email', 'door_no', 'shop_no', 'complex_name',
            'building_name', 'street_name', 'area', 'pincode', 'city', 'state', 'location_guide',
            'kyc_details'
        ]

    def create(self, validated_data):
        user = self.context.get('request').user if self.context.get('request') else None
        if user is None or user.role_name not in ["super_admin", "admin", "Project Owner", "Super User"]:
            raise serializers.ValidationError("You do not have permission to create a Business Partner.")
        validated_data['user_id'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
