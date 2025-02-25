from rest_framework import generics, status, response
from rest_framework.exceptions import NotFound
from .models import Order
from user.models import ResUser as user
from .serializers import OrderSerializer, OrderUpdateSerializer, BackSellerOrderUpdateSerializer
from .models import current_user, filter_queryset
from rest_framework.response import Response

# Helper function to check if user role is valid
def is_valid_user_role(user):
    """
    Check if the user's role is one of the allowed roles:
    'admin', 'staff', 'seller', 'customer'.
    """
    valid_roles = ['admin', 'staff', 'seller', 'customer']
    return user.role_name in valid_roles

class SallerFetchOrderAPI(generics.GenericAPIView):
    serializer_class = None  # Optional, can define a serializer
    queryset = Order.objects.all()

    def get(self, request):
        """
        Fetch all pending orders if the user is a seller or other valid user roles.
        """
        current_user = request.user.id
        try:
            obj = user.objects.get(id=current_user)
            if is_valid_user_role(obj):  # Checking if the user role is valid
                orders = Order.objects.filter(state='draft')
                return response.Response(orders.values(), status=status.HTTP_200_OK)
        except user.DoesNotExist:
            return response.Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return response.Response({"detail": "Unauthorized or invalid role"}, status=status.HTTP_403_FORBIDDEN)

class AssignToCraftsmanSallerUpdateOrderAPI(generics.GenericAPIView):
    serializer_class = OrderUpdateSerializer
    queryset = Order.objects.all()

    def put(self, request, orderid):
        """
        Update the state of an order by order ID.
        """
        current_user = request.user.id
        try:
            obj = user.objects.get(id=current_user)
            if is_valid_user_role(obj):  # Checking if the user role is valid
                try:
                    order = Order.objects.get(id=orderid)
                    # Set the context to pass the state to the serializer
                    serializer = self.serializer_class(data=request.data, context={'state': request.data.get('state', 'rejected')})
                    serializer.is_valid(raise_exception=True)
                    
                    new_state = serializer.validated_data['state']
                    new_user_selection = serializer.validated_data.get('selection', None)

                    if new_state == 'rejected':
                        if 'text' not in serializer.validated_data:
                            return response.Response({"detail": "Text is required for rejected orders"}, status=status.HTTP_400_BAD_REQUEST)

                    if new_state in ['accepted', 'rejected']:   
                        order.state = new_state
                        
                        # If 'accepted', assign the user selection (if present)
                        if new_state == 'accepted' and new_user_selection:
                            user_updated_id = user.objects.get(id=new_user_selection)
                            order.user_id = user_updated_id  # Assign first value if it's a list
                        order.save()

                        return response.Response({"detail": f"Order state updated to {new_state}"}, status=status.HTTP_200_OK)
                    
                    return response.Response({"detail": "Invalid state value"}, status=status.HTTP_400_BAD_REQUEST)
                except Order.DoesNotExist:
                    return response.Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except user.DoesNotExist:
            return response.Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return response.Response({"detail": "Unauthorized or invalid role"}, status=status.HTTP_403_FORBIDDEN)

class AssignToBackSellerOrderAPI(generics.GenericAPIView):
    serializer_class = BackSellerOrderUpdateSerializer
    queryset = Order.objects.all()

    def put(self, request, orderid):
        """
        Update the state of an order by order ID.
        """
        current_user = request.user.id
        try:
            obj = user.objects.get(id=current_user)
            if is_valid_user_role(obj):  # Checking if the user role is valid
                try:
                    order = Order.objects.get(id=orderid)
                    # Set the context to pass the state to the serializer
                    serializer = self.serializer_class(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    new_state = serializer.validated_data['state']
                    start_date = serializer.validated_data.get('start_date', None)
                    end_date = serializer.validated_data.get('end_date', None)
                    text = serializer.validated_data.get('text', None)
                    if new_state in ['accepted', 'rejected']:
                        if new_state == 'accepted':   
                            order.state = 'progress'
                            order.start_date = start_date
                            order.end_date= end_date
                            order.text_assign_user=None
                            order.user_id = obj
                            order.save()
                        else:
                            if new_state == 'rejected':
                                order.state = 'draft'
                                order.text_assign_user = text + " " + " User Name" + obj.first_name + " " + obj.last_name
                                order.user_id = None
                                order.save()
                                return response.Response({"detail": "Order is not accepted"}, status=status.HTTP_400_BAD_REQUEST)
                        return response.Response({"detail": f"Order state updated to {new_state}"}, status=status.HTTP_200_OK)
                    return response.Response({"detail": "Invalid state value"}, status=status.HTTP_400_BAD_REQUEST)
                except Order.DoesNotExist:
                    return response.Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except user.DoesNotExist:
            return response.Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return response.Response({"detail": "Unauthorized or invalid role"}, status=status.HTTP_403_FORBIDDEN)

class OrderAPI(generics.GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_user_and_type(self, request):
        """
        Retrieve the current user and their type.
        """
        return current_user(request)

    def get_filtered_queryset(self, user, user_type):
        """
        Filters the queryset based on the user type.
        """
        return filter_queryset(user, user_type)

    def is_valid_user_role(self, user):
        """
        Check if the user's role is one of the allowed roles:
        'admin', 'staff', 'seller', 'customer'.
        """
        valid_roles = ['admin', 'staff', 'seller', 'customer']
        return user.role_name in valid_roles

    def post(self, request):
        """
        Create a new order.
        """
        user, user_type = self.get_user_and_type(request)
        
        # Check if the user role is valid before proceeding with order creation
        if not self.is_valid_user_role(user):
            return response.Response(
                {"error": "You do not have permission to create orders."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        self.queryset = self.get_filtered_queryset(user, user_type)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Check for duplicate order by order_no
        order_no = serializer.validated_data.get('order_no')
        if Order.objects.filter(order_no=order_no).exists():
            return response.Response(
                {"error": "An order with this order_no already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
# Ensure default state is 'draft'
        serializer.validated_data['state'] = 'draft'

        # Create the order and link it to the user
        order = serializer.save()
        return response.Response(
            self.serializer_class(order).data, status=status.HTTP_201_CREATED
        )

    def get(self, request, id=None):
        """
        Retrieve one or multiple orders.
        """
        user, user_type = self.get_user_and_type(request)
        self.queryset = self.get_filtered_queryset(user, user_type)

        if id:
            try:
                order = self.queryset.get(id=id)
            except Order.DoesNotExist:
                raise NotFound("Order not found")
            serializer = self.serializer_class(order)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            orders = self.queryset
            serializer = self.serializer_class(orders, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        """
        Update an order's details.
        """
        user, user_type = self.get_user_and_type(request)
        self.queryset = self.get_filtered_queryset(user, user_type)

        try:
            order = self.queryset.get(id=id)
        except Order.DoesNotExist:
            raise NotFound("Order not found")

        serializer = self.serializer_class(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """
        Delete an order.
        """
        user, user_type = self.get_user_and_type(request)
        self.queryset = self.get_filtered_queryset(user, user_type)

        try:
            order = self.queryset.get(id=id)
        except Order.DoesNotExist:
            raise NotFound("Order not found")

        order.delete()
        return response.Response(
            {"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
