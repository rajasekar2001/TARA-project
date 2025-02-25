from django.db import models
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from user.models import ResUser  # Ensure correct import of user model
import requests
import logging
import re

logger = logging.getLogger(__name__)



ROLE_CHOICES = ['super_admin', 'Project Owner', 'admin', 'Super User']

def validate_pan_number(value):
    """
    Validates if the given value is a valid PAN number (Permanent Account Number - India).
    The format should be: 5 uppercase letters, followed by 4 digits, followed by 1 uppercase letter.
    Example: ABCDE1234F
    """
    pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'

    if not re.match(pan_pattern, value):
        raise ValidationError(
            f"'{value}' is not a valid PAN number. It should be in the format: ABCDE1234F."
        )
#gst validator
def validate_gst_number(value):
    """
    Validates if the given value is a valid GSTIN (Goods and Services Tax Identification Number - India).
    The format should be: 2-digit state code + 10-character PAN + 1 entity code + 'Z' + 1 checksum character.
    Example: 22AAAAA1234A1Z5
    """
    gst_pattern = r'^[0-3][0-9][A-Z]{5}[0-9]{4}[A-Z][0-9A-Z]Z[0-9A-Z]$'

    if not re.match(gst_pattern, value):
        raise ValidationError(
            f"'{value}' is not a valid GST number. It should be in the format: 22AAAAA1234A1Z5."
        )
    
#Aadhar card validator
def validate_aadhar_no(value):
    if not re.match(r'^[0-9]{12}$', value):
        raise ValidationError(_("Invalid Aadhar Number. It must be exactly 12 digits."))
    
# IFSC validator 
def validate_ifsc_code(value):
    ifsc_pattern = r'^[A-Z]{4}[0-9]{7}$'
    if not re.match(ifsc_pattern, value):
        raise ValidationError(_("Invalid IFSC Code. Expected format: ABCD0123456."))

# Mobile Number Validator
def validate_mobile_no(value):
    if not value.isdigit():
        raise ValidationError(_("Mobile number must contain only digits."))
    if not (10 <= len(value) <= 15):
        raise ValidationError(_("Mobile number must be between 10 to 15 digits."))
    
# msme number validator
def validate_msme_no(value):
    """
    Validate MSME (Udyog Aadhaar) number.
    Format: UDY + 2-digit number + 3 uppercase letters + 7-digit number
    Example: UDY12ABC1234567
    """
    msme_pattern = r'^[Uu][Dd][Yy]\d{2}[A-Za-z]{3}\d{7}$'  # Updated pattern
    
    if not re.fullmatch(msme_pattern, value):
        raise ValidationError("Invalid MSME format. Expected format: UDY12ABC1234567.")

    return value  # Return value if validation passes

class BusinessPartner(models.Model):
    user_id = models.ForeignKey(ResUser, on_delete=models.CASCADE, related_name='BusinessPartner', blank=True, null=True)
    bp_code = models.CharField(max_length=50, unique=True)
    term = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=255)

    # Contact Details
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15, validators=[validate_mobile_no], verbose_name="Mobile No", unique=True)
    alternate_mobile = models.CharField(max_length=15, validators=[validate_mobile_no], blank=True, null=True,unique=True)
    landline = models.CharField(max_length=15, blank=True, null=True)
    business_email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True,unique=True)

    # Address Details
    door_no = models.CharField(max_length=50, blank=True, null=True)
    shop_no = models.CharField(max_length=50, blank=True, null=True)
    complex_name = models.CharField(max_length=255, blank=True, null=True)
    building_name = models.CharField(max_length=255, blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    location_guide = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user_id and self.user_id.role_name not in ROLE_CHOICES:
            raise PermissionDenied("You do not have permission to create a Business Partner.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bp_code} - {self.business_name}"

class BusinessPartnerKYC(models.Model):
    bp_code = models.ForeignKey(
        BusinessPartner, on_delete=models.CASCADE, related_name='kyc_details'
    )  # One-to-Many Relationship 

    # KYC Details
    bis_no = models.CharField(max_length=50, blank=True, null=True)
    gst_no = models.CharField(max_length=50,validators=[validate_gst_number], blank=True, null=True)
    msme_no = models.CharField(max_length=50, validators=[validate_msme_no], blank=True, null=True)
    pan_card_image = models.ImageField(upload_to='pan_card', blank=True, null=True)
    pan_no = models.CharField(max_length=10, blank=True, null=True, validators=[validate_pan_number])  # Apply the validator here    
    tan_no = models.CharField(max_length=10, validators=[validate_pan_number], blank=True, null=True)

    # Aadhar Details
    aadhar_no = models.CharField(max_length=12, validators=[validate_aadhar_no],blank=True, null=True)
    aadhar_front_image = models.ImageField(upload_to='kyc/aadhar/', blank=True, null=True)
    aadhar_back_image = models.ImageField(upload_to='kyc/aadhar/', blank=True, null=True)
    

    # Bank Details
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=50, blank=True, null=True)
    branch = models.CharField(max_length=255, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20,validators=[validate_ifsc_code], blank=True, null=True)
    bank_city = models.CharField(max_length=100, blank=True, null=True)
    bank_state = models.CharField(max_length=100, blank=True, null=True)

    note = models.TextField(blank=True, null=True)

def save(self, *args, **kwargs):
        if not self.ifsc_code and self.bank_name and self.branch:
            fetched_ifsc = fetch_ifsc_code(self.bank_name, self.branch)
            if fetched_ifsc:
                self.ifsc_code = fetched_ifsc
            else:
                logger.warning(f"Could not fetch IFSC Code for {self.bank_name}, {self.branch}. Please enter manually.")
        super().save(*args, **kwargs)
        

def fetch_ifsc_code(bank_name, branch):
    """
    Fetch IFSC Code based on Bank Name and Branch using an external API.
    """
    try:
        url = f"https://ifsc.razorpay.com/{bank_name}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("IFSC")
        else:
            logger.warning(f"Failed to fetch IFSC Code for {bank_name}, {branch}. API Response: {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching IFSC Code: {str(e)}")
        return None 

def fetch_location_from_pincode(pincode):
    if not pincode or not pincode.isdigit() or len(pincode) != 6:
        return None, None
    url = f"https://api.postalpincode.in/pincode/{pincode}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data and data[0]['Status'] == "Success" and data[0]['PostOffice']:
            city = data[0]['PostOffice'][0].get('District', '')
            state = data[0]['PostOffice'][0].get('State', '')
            return city, state
        else:
            logger.warning(f"Invalid pincode response: {data[0].get('Message', 'Unknown error')}")
            return None, None
    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
    return None, None

@receiver(pre_save, sender=BusinessPartner)
def fetch_location_pre_save(sender, instance, **kwargs):
    if instance.pincode and (not instance.city or not instance.state):
        city, state = fetch_location_from_pincode(instance.pincode)
        instance.city = city
        instance.state = state