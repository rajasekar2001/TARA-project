from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'customer_no', 'name', 'address', 'city', 'state', 'country',
            'pincode', 'phone', 'email', 'gst_no', 'pan_no', 'created_at', 'updated_at'
        ]
        read_only_fields = ['customer_no', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Custom create method to handle auto-generating the customer number.
        """
        customer = Customer.objects.create(**validated_data)
        customer.save()  # This triggers the model's `save` method for customer_no generation
        return customer

    def update(self, instance, validated_data):
        """
        Custom update method to handle updates to the Customer instance.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # Ensure the `save` method in the model is called for consistency
        return instance
