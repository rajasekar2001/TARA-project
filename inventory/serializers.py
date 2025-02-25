from rest_framework import serializers
from .models import RawMaterial, FinishedProduct, Production

# Raw Material Serializer
class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = ['id', 'name', 'sku', 'quantity', 'unit_price']

# Finished Product Serializer
class FinishedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedProduct
        fields = ['id', 'name', 'sku', 'quantity', 'unit_price']

# Production Serializer (Handles Raw Material Consumption & Finished Goods Creation)
class ProductionSerializer(serializers.ModelSerializer):
    raw_material_name = serializers.CharField(source='raw_material.name', read_only=True)
    finished_product_name = serializers.CharField(source='finished_product.name', read_only=True)

    class Meta:
        model = Production
        fields = ['id', 'raw_material', 'raw_material_name', 'finished_product', 'finished_product_name', 'raw_material_used', 'quantity_produced', 'created_at']

    def create(self, validated_data):
        """Custom logic to manage inventory when a production order is created."""
        raw_material = validated_data['raw_material']
        finished_product = validated_data['finished_product']
        raw_material_used = validated_data['raw_material_used']
        quantity_produced = validated_data['quantity_produced']

        if raw_material.quantity < raw_material_used:
            raise serializers.ValidationError("Not enough raw material available!")

        # Deduct raw material
        raw_material.quantity -= raw_material_used
        raw_material.save()

        # Add finished goods
        finished_product.quantity += quantity_produced
        finished_product.save()

        return super().create(validated_data)
