from rest_framework import serializers
from .models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order_no', 'product_name', 'quantity', 'price', 'category', 'order_status']
