from rest_framework import generics, status, response
from rest_framework.exceptions import NotFound
from .models import Customer
from user.models import ResUser
from .serializers import CustomerSerializer

class CustomerAPI(generics.GenericAPIView):
    serializer_class = CustomerSerializer 
    queryset = Customer.objects.filter(user__role_name__in=["customer", "One Time User"])

    def post(self, request):
        """
        Create a new customer.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Ensure that user exists and has the allowed role
        try:
            user = ResUser.objects.get(id=request.data.get('user'), role_name__in=["customer", "One Time User"])
        except ResUser.DoesNotExist:
            return response.Response({"error": "Invalid user or role"}, status=status.HTTP_400_BAD_REQUEST)
        
        customer, created = Customer.objects.update_or_create(user=user, defaults=serializer.validated_data)
        return response.Response(self.serializer_class(customer).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def get(self, request, id=None):
        """
        Retrieve Customer(s).
        """
        if id:
            customer = self.get_customer(id)
            serializer = self.serializer_class(customer)
        else:
            customers = Customer.objects.filter(user__role_name__in=["customer", "One Time User"])
            serializer = self.serializer_class(customers, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        """
        Update Customer details.
        """
        customer = self.get_customer(id)
        serializer = self.serializer_class(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """
        Delete a Customer.
        """
        customer = self.get_customer(id)
        customer.delete()
        return response.Response({"message": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def get_customer(self, id):
        """
        Utility method to get a customer or raise NotFound.
        """
        try:
            return Customer.objects.get(id=id, user__role_name__in=["customer", "One Time User"])
        except Customer.DoesNotExist:
            raise NotFound("Customer not found")
