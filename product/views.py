from rest_framework import generics, status, response
from rest_framework.exceptions import NotFound
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer

class ProductImageAPI(generics.GenericAPIView):
    """
    API to upload images for a product.
    """
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()

    def post(self, request):
        """
        Create a new product image.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Use the 'product' field instead of 'product_id'
        product_id = request.data.get('product')
        
        if not product_id:
            return response.Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch product based on 'product_id' (product is the primary key field)
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

        # Save image with product link
        serializer.save(product=product)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductAPI(generics.GenericAPIView):
    """
    API to handle Product CRUD operations.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def post(self, request):
        """
        Create a new Product.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # `product_id` automatically generate hota hai, isliye check nahi kiya
        product = serializer.save()
        return response.Response(self.serializer_class(product).data, status=status.HTTP_201_CREATED)

    def get(self, request, product_id=None):
        """
        Retrieve Product(s).
        """
        if product_id:
            try:
                product = Product.objects.get(product_id=product_id)
            except Product.DoesNotExist:
                raise NotFound("Product not found")
            serializer = self.serializer_class(product)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            products = Product.objects.all()
            serializer = self.serializer_class(products, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        """
        Update Product details.
        """
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

        serializer = self.serializer_class(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        """
        Delete a Product.
        """
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

        product.delete()
        return response.Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
