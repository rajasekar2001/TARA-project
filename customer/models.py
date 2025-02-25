from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import ResUser  # Import the User model

class Customer(models.Model):
    """
    Customer model to store customer details.
    """
    user = models.OneToOneField(ResUser,on_delete=models.CASCADE,related_name="customer",null=True,blank=True,limit_choices_to={"role_name__in": ["customer", "One Time User"]})  # Restrict user choices
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="Customer/Profile", blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Customer: {self.full_name} ({self.user.username if self.user else 'No User'})"

@receiver(post_save, sender=ResUser)
def create_or_update_customer(sender, instance, created, **kwargs):
    if instance.role_name in ["customer", "One Time User"]:
        customer_data = {
            "phone": instance.mobile_no,
            "email": instance.email_id,
            "full_name": instance.full_name,
            "dob": instance.dob,
            "gender": instance.gender,
            "profile_picture": instance.profile_picture,
            "city": instance.city,
            "state": instance.state,
            "country": instance.country,
            "pincode": instance.pincode,
        }

        customer, _ = Customer.objects.update_or_create(user=instance, defaults=customer_data)
