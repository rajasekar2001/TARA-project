from django.utils import timezone
import pytz
from rest_framework import serializers
from .models import Order
from user.models import ResUser, BusinessPartner  
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from datetime import date



class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Order model.
    """
    bp_code = serializers.SlugRelatedField(
        queryset=BusinessPartner.objects.all(),
        slug_field='bp_code',
        required=False,
        allow_null=True
    )
    order_date = serializers.SerializerMethodField() 
       
    def get_order_date(self, obj):
        ist = pytz.timezone('Asia/Kolkata')
        return obj.order_date.astimezone(ist).strftime('%d-%m-%Y %H:%M:%S IST')
    class Meta:
        model = Order
        fields = [
            'order_image', 'order_no', 'bp_code', 'name', 'reference_no', 'order_date', 'due_date', 'category', 'order_type',
            'quantity', 'weight', 'dtype', 'branch_code', 'product', 'design', 'vendor_design', 'barcoded_quality',
            'supplied', 'balance', 'assigned_by', 'narration', 'note', 'sub_brand', 'make', 'work_style', 'form',
            'finish', 'theme', 'collection', 'description', 'assign_remarks', 'screw', 'polish', 'metal_colour',
            'purity', 'stone', 'hallmark', 'rodium', 'enamel', 'hook', 'size', 'open_close', 'length', 'hbt_class',
            'console_id', 'tolerance_from', 'tolerance_to'
        ]
        read_only_fields = ['order_no', 'order_date'] 

    def create(self, validated_data):
        if 'bp_code' not in validated_data:
            raise serializers.ValidationError({"bp_code": "This field is required."})
        return super().create(validated_data)

    def to_representation(self, instance):
        """Modify the output representation to include business_name with bp_code."""
        data = super().to_representation(instance)
        if instance.bp_code:
            data['bp_code'] = f"{instance.bp_code.bp_code}-{instance.bp_code.business_name}"
        return data
    
    def validate(self, data):
        if 'order_date' in data:
            raise serializers.ValidationError("Order date is auto-set to today's date")
        return data
    
    def validate_due_date(self, value):
        """
        Validate that due_date is at least tomorrow (future date only).
        """
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        
        if value <= today:
            raise serializers.ValidationError("Due date must be tomorrow or later. Cannot be today or in the past.")
        return value
    
    def create(self, validated_data):
        if 'bp_code' not in validated_data:
            raise serializers.ValidationError({"bp_code": "This field is required."})
        last_order = Order.objects.all().order_by('id').last()
        
        if not last_order:
            new_order_no = '001'
        else:
            try:
                last_number = int(last_order.order_no)
                new_number = last_number + 1
                new_order_no = f"{new_number:03d}"
            except (ValueError, AttributeError):
                new_order_no = f"{Order.objects.count() + 1:03d}"
        
        validated_data['order_no'] = new_order_no
        return super().create(validated_data)




class OrderUpdateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=[
        ('accepted', 'Accepted'), ('rejected', 'Rejected')
    ])
    text = serializers.CharField(max_length=255, required=False)
    selection = serializers.ChoiceField(choices=[], required=False)
    flag = serializers.HiddenField(default='flag')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = ResUser.objects.filter(role_name='craftsman')
        if self.context.get('state') != 'rejected':
            self.fields['selection'].choices = [(user.id, user.username) for user in users]
        else:
            self.fields.pop('selection', None)


class BackSellerOrderUpdateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=[
        ('accepted', 'Accepted'), ('rejected', 'Rejected')
    ])
    text = serializers.CharField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)



class AssignOrdersSerializer(serializers.Serializer):
    craftsman_id = serializers.IntegerField()
    order_ids = serializers.ListField(child=serializers.IntegerField(), min_length=1)

    def validate(self, data):
        """
        Validate if craftsman exists and orders are valid.
        """
        craftsman = ResUser.objects.filter(id=data['craftsman_id'], role_name='craftsman').first()
        if not craftsman:
            raise serializers.ValidationError("Invalid Craftsman ID")
        orders = Order.objects.filter(id__in=data['order_ids'], state='new')
        if not orders.exists():
            raise serializers.ValidationError("No valid new orders selected")
        data['craftsman'] = craftsman
        data['orders'] = orders
        return data
    def save(self):
        """
        Assign selected orders to the craftsman.
        """
        craftsman = self.validated_data['craftsman']
        orders = self.validated_data['orders']
        orders.update(craftsman=craftsman, state='assigned')
        return orders
class CraftsmanSerializer(serializers.ModelSerializer):
    """Serializer for listing available craftsmen."""
    class Meta:
        model = ResUser
        fields = ['id', 'username']

class OrderCraftsmanSerializer(serializers.ModelSerializer):
    """Serializer for listing all orders."""
    craftsman = CraftsmanSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'created_at', 'craftsman']
        
class OrderStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating order status by craftsman."""
    order_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=[('in-process', 'In Process')])

    def validate(self, data):
        """Validate order exists and is assigned to the craftsman."""
        request = self.context.get('request')
        user = request.user if request else None

        if not user or user.role_name != 'craftsman':
            raise serializers.ValidationError("Only craftsmen can update orders.")

        try:
            order = Order.objects.get(id=data['order_id'], craftsman=user, state='assigned')
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found or not assigned to you.")

        data['order'] = order
        return data

    def update(self, instance, validated_data):
        """Update order state to in-process."""
        instance.state = 'in-process'
        instance.save()
        return instance
    
class ApproveOrderSerializer(serializers.Serializer):
    """
    Serializer for craftsmen to mark an order as completed and for Admin/Super Admin to approve.
    """
    order_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=[
        ("completed_by_craftsman", "Completed by Craftsman"),
        ("approved", "Approved by Admin"),
    ])

    def validate(self, data):
        """Validate order state and user role."""
        user = self.context['request'].user

        try:
            order = Order.objects.get(id=data['order_id'])
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found.")

        if data['status'] == "completed_by_craftsman":
            # Craftsman can only mark their own orders as completed
            if order.craftsman != user:
                raise serializers.ValidationError("You can only mark your own orders as completed.")
            if order.state != "assigned":
                raise serializers.ValidationError("Only assigned orders can be marked as completed.")

        elif data['status'] == "approved":
            # Only Admin/Super Admin can approve completed orders
            if user.role_name not in ["admin", "super_admin"]:
                raise serializers.ValidationError("Only Admin or Super Admin can approve orders.")
            if order.state != "completed_by_craftsman":
                raise serializers.ValidationError("Only completed orders can be approved.")

        return data

    def update(self, instance, validated_data):
        """Update the order status."""
        order = Order.objects.get(id=validated_data['order_id'])
        order.state = validated_data['status']
        order.save()
        return order


class CompletedOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for listing completed orders.
    """
    craftsman = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'name', 'reference_no', 'craftsman', 'state']


class OrderRejectSerializer(serializers.ModelSerializer):
    """
    Serializer for listing orders with status.
    """
    craftsman = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'name', 'reference_no', 'craftsman', 'state']


@receiver(post_save, sender=ResUser)
def assign_bp_code_to_orders(sender, instance, created, **kwargs):
    """Assign user's bp_code to their orders when a new user is created."""
    if created and instance.bp_code:
        Order.objects.filter(user=instance).update(bp_code=instance.bp_code)
        
        
@receiver(post_save, sender=Order)
def set_order_date(sender, instance, created, **kwargs):
    if created and not instance.order_date:
        instance.order_date = date.today()
        instance.save()