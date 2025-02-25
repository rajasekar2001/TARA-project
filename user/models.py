from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import logging
import requests

logger = logging.getLogger(__name__)

def validate_mobile_no(value):
    """Ensure mobile number contains only digits and is 10-15 digits long."""
    if not value.isdigit():
        raise ValidationError(_("Mobile number must contain only digits."))
    if not (10 <= len(value) <= 15):
        raise ValidationError(_("Mobile number must be between 10 to 15 digits."))

class ResUser(AbstractUser):
    """Custom user model extending AbstractUser with role-based access and permissions."""

    ROLE_CHOICES = [
        ('super_admin', 'Project Owner'),
        ('admin', 'Super User'),
        ('staff', 'Key User'),
        ('craftsman', 'Craftsman'),
        ('seller', 'End User'),
        ('customer', 'One Time User'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    USER_TYPE_CHOICES = [
        ('internal', 'INTERNAL USER'),
        ('external', 'EXTERNAL USER'),
    ]
    profile_picture = models.ImageField(upload_to='User/Profile', blank=True, null=True, verbose_name=_("Profile Picture"))
    user_code = models.CharField(max_length=25, unique=True, null=True, blank=True, verbose_name=_("User Code"))
    role_name = models.CharField(max_length=50, choices=ROLE_CHOICES, default='super_admin', verbose_name=_("Role Name"))
    user_state = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='internal', verbose_name=_("User State"))
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    mobile_no = models.CharField(max_length=15, validators=[validate_mobile_no], verbose_name=_("Mobile Number"))
    email_id = models.EmailField(unique=True, null=True, validators=[EmailValidator(message=_("Enter a valid email address."))], verbose_name=_("Email ID"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name=_("Status"))
    dob = models.DateField(blank=True, null=True, verbose_name=_("Date of Birth"))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name=_("Gender"))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("City"))
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("State"))
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Country"))
    pincode = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Pincode"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    # Permissions
    view_only = models.BooleanField(default=False, verbose_name=_("View Only"))
    copy = models.BooleanField(default=False, verbose_name=_("Copy"))
    screenshot = models.BooleanField(default=False, verbose_name=_("Screenshot"))
    print_perm = models.BooleanField(default=False, verbose_name=_("Print"))
    download = models.BooleanField(default=False, verbose_name=_("Download"))
    share = models.BooleanField(default=False, verbose_name=_("Share"))
    edit = models.BooleanField(default=False, verbose_name=_("Edit"))
    delete_perm = models.BooleanField(default=False, verbose_name=_("Delete"))  # Changed to avoid method conflicts
    manage_roles = models.BooleanField(default=False, verbose_name=_("Manage Roles"))
    approve = models.BooleanField(default=False, verbose_name=_("Approve"))
    reject = models.BooleanField(default=False, verbose_name=_("Reject"))
    archive = models.BooleanField(default=False, verbose_name=_("Archive"))
    restore_perm = models.BooleanField(default=False, verbose_name=_("Restore"))  # Changed to avoid method conflicts
    transfer = models.BooleanField(default=False, verbose_name=_("Transfer"))
    custom_access = models.BooleanField(default=False, verbose_name=_("Custom Access"))
    full_control = models.BooleanField(default=False, verbose_name=_("Full Control"))

    # Soft delete flag
    delete_flag = models.BooleanField(default=False, verbose_name=_("Soft Deleted"))

    # Relationship with Django Groups for RBAC
    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    def soft_delete(self):
        """Marks the user as soft deleted."""
        self.delete_flag = True
        self.save(update_fields=['delete_flag'])

    def restore_user(self):
        """Restores a soft-deleted user."""
        self.delete_flag = False
        self.save(update_fields=['delete_flag'])

    def save(self, *args, **kwargs):
        """Override save method to handle soft delete and permission assignment."""
        self.set_default_role_for_external_user()
        super().save(*args, **kwargs)
        self.assign_role_permissions()

    def set_default_role_for_external_user(self):
        """Set default role for external users."""
        if self.user_state == 'external' and self.role_name != 'staff':
            self.role_name = 'staff'

    def assign_role_permissions(self):
        """Assign permissions based on user role."""
        if not self.pk:
            return

        role_group, created = Group.objects.get_or_create(name=self.role_name)
        self.groups.add(role_group)

        permissions_map = {
            'view_only': 'view',
            'copy': 'copy',
            'screenshot': 'screenshot',
            'print_perm': 'print',
            'download': 'download',
            'share': 'share',
            'edit': 'edit',
            'delete_perm': 'delete',
            'manage_roles': 'manage_roles',
            'approve': 'approve',
            'reject': 'reject',
            'archive': 'archive',
            'restore_perm': 'restore',
            'transfer': 'transfer',
            'custom_access': 'custom_access',
            'full_control': 'full_control',
        }

        assigned_permissions = [
            Permission.objects.get(codename=codename)
            for field, codename in permissions_map.items()
            if getattr(self, field, False) and Permission.objects.filter(codename=codename).exists()
        ]

        self.user_permissions.set(assigned_permissions)


def fetch_location_pre_save(sender, instance, **kwargs):
    """Fetch city, state, and country based on pincode."""
    if instance.pincode:
        url = f"https://api.postalpincode.in/pincode/{instance.pincode}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data and data[0]['Status'] == "Success" and data[0]['PostOffice']:
                instance.city = data[0]['PostOffice'][0].get('District', '')
                instance.state = data[0]['PostOffice'][0].get('State', '')
                instance.country = "India"
            else:
                instance.city = None
                instance.state = None
                instance.country = None
                logger.warning(f"Invalid pincode data: {data[0].get('Message', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching location for pincode {instance.pincode}: {str(e)}")
            instance.city = None
            instance.state = None
            instance.country = None

models.signals.pre_save.connect(fetch_location_pre_save, sender=ResUser)


class RoleDashboardMapping(models.Model):
    """Mapping between roles and dashboard URLs."""
    role = models.CharField(max_length=50, choices=ResUser.ROLE_CHOICES)
    dashboard_url = models.URLField()

    def __str__(self):
        return f'{self.role} - {self.dashboard_url}'
