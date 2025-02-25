from rest_framework import serializers
from .models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for handling product images."""
    
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)  # Product ID is now optional
    
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model including images."""
    
    images = ProductImageSerializer(many=True, required=False)  # Allow writing images

    class Meta:
        model = Product
        fields = ['product_id', 'category', 'quantity', 'price', 'status', 'images']
        read_only_fields = ['product_id', 'status']

    def create(self, validated_data):
        """
        Override create method to handle product images.
        """ 
        request = self.context.get('request')  # Safely get request from context
        images_data = request.FILES.getlist('images') if request else []

        images = validated_data.pop('images', []) if 'images' in validated_data else []

        product = Product.objects.create(**validated_data)

        # Save images if provided
        for image in images:
            ProductImage.objects.create(product=product, image=image['image'])

        for image_file in images_data:
            ProductImage.objects.create(product=product, image=image_file)

        product.status = 'In Stock' if product.quantity > 0 else 'Out of Stock'
        product.save()
        return product

    def update(self, instance, validated_data):
        """
        Override update method to update product and images.
        """
        images_data = self.context['request'].FILES.getlist('images')  # Get images from request

        images = validated_data.pop('images', []) if 'images' in validated_data else []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if images or images_data:
            instance.images.all().delete()  # Delete old images
            
            for image in images:
                ProductImage.objects.create(product=instance, image=image['image'])

            for image_file in images_data:
                ProductImage.objects.create(product=instance, image=image_file)

        instance.status = 'In Stock' if instance.quantity > 0 else 'Out of Stock'
        instance.save()
        return instance
