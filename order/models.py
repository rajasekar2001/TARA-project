from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import ResUser as user


def get_order_no():
    last_order = Order.objects.order_by('-id').first()
    if last_order and last_order.order_no.startswith('WR'):
        order_number = int(last_order.order_no[2:]) + 1
        return f"WR{order_number:03d}"
    return "WR001"

def current_user(request):
    current_user = user.objects.get(id=request.user.id)
    user_type = current_user.ROLE_CHOICES
    return current_user, user_type

def filter_queryset(user, user_type):
    if user_type in ['customer', 'staff']:
        return Order.objects.filter(user=user)
    elif user_type == 'admin':
        return Order.objects.filter(user=user)
    elif user_type == 'superadmin':
        return Order.objects.all()
    else:
        return Order.objects.none()

# @staticmethod
# def get_current_user(request):
#     """
#     Get current user and their type from request object.
#     """
#     user = request.user
#     if user.is_authenticated:
#         user_type = None
#         if hasattr(user, 'user_type'):
#             user_type = user.user_type  # Fetch user_type (customer, staff, admin, superadmin)

#         if user_type == 'customer':
#             user = user.customer
#         elif user_type == 'staff':
#             user = user.staff
#         elif user_type == 'admin':
#             user = user.admin
#         elif user_type == 'superadmin':
#             user = user.superadmin

#         return user, user_type  # Return both user and user_type
#     else:
#         raise Exception("User not authenticated")
        
class Order(models.Model):
    SIZE_CHOICES = [
        ('Large', 'Large'),
        ('Medium', 'Medium'),
        ('Small', 'Small'),
    ]

    SCREW_CHOICES = [
        ('Closed', 'Closed'),
        ('Open', 'Open'),
    ]

    HOOK_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    RODIUM_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    HALLMARK_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    STONE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    CATEGORY_CHOICES = [
        ('Rings', 'Rings'),
        ('Chains', 'Chains'),
        ('Pendants', 'Pendants'),
        ('Bangles', 'Bangles'),
        ('Anklets', 'Anklets'),
        ('Necklaces', 'Necklaces'),
        ('Bracelets', 'Bracelets'),
        ('Earrings', 'Earrings'),
    ]

    WEIGHT_UNIT_CHOICES = [
        ('mg', 'Milligram'),
        ('g', 'Gram'),
        ('kg', 'Kilogram'),
        ('oz', 'Ounce'),
        ('lb', 'Pound'),
    ]
    STATE_CHOICES=[('draft','Draft'),('pending','Pending'),('approved','Approved'),('accepted','accepted'),('progress','in progress'),('rejected','Rejected')]
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    order_no = models.CharField(max_length=100, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight_unit = models.CharField(max_length=2, choices=WEIGHT_UNIT_CHOICES, blank=True, null=True)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES, blank=True, null=True)
    stone = models.CharField(max_length=50, choices=STONE_CHOICES, blank=True, null=True)
    rodium = models.CharField(max_length=50, choices=RODIUM_CHOICES, blank=True, null=True)
    hallmark = models.CharField(max_length=50, choices=HALLMARK_CHOICES, blank=True, null=True)
    screw = models.CharField(max_length=50, choices=SCREW_CHOICES, blank=True, null=True)
    hook = models.CharField(max_length=50, choices=HOOK_CHOICES, blank=True, null=True)
    narration = models.TextField(blank=True, null=True)
    order_image = models.ImageField(upload_to='order_images/', blank=True, null=True)
    due_date = models.DateField()
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField(blank=True, null=True, verbose_name=_("Start Date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("End Date"))
    text_assign_user = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = get_order_no()
        super().save(*args, **kwargs)


    def __str__(self):
        weight_display = f"{self.weight}{self.weight_unit}" if self.weight and self.weight_unit else "No weight specified"
        return f"Order {self.order_no}-{self.category}-{weight_display}"
