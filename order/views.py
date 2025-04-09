from django.shortcuts import get_object_or_404
from rest_framework import generics, status, response
from rest_framework.exceptions import NotFound
from .models import Order, BusinessPartner
from user.models import ResUser as user
from .serializers import OrderSerializer, OrderUpdateSerializer, BackSellerOrderUpdateSerializer, CraftsmanSerializer, OrderCraftsmanSerializer, OrderStatusUpdateSerializer, ApproveOrderSerializer, CompletedOrderSerializer, OrderRejectSerializer
from .models import current_user, filter_queryset
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from user.models import ResUser
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()



# Helper function to check if user role is valid
def is_valid_user_role(user): 
    """
    Check if the user's role is one of the allowed roles:
    'admin', 'staff', 'seller', 'customer'.
    """
    # valid_roles = ['admin', 'staff', 'seller', 'customer']
    valid_roles = ['Super Admin', 'Admin', 'User']
    return user.role_name in valid_roles


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all Business Partners or filter by `bp_code`.
        """
        bp_code = request.query_params.get("bp_code")
        queryset = self.get_queryset().filter(bp_code=bp_code) if bp_code else self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new order with status set to 'in-process'.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Set the status to 'in-process' before saving
            serializer.validated_data['status'] = 'in-process'
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class OrderList(generics.GenericAPIView):
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        Get all Business Partners or filter by `bp_code`.
        """
        bp_code = request.query_params.get("bp_code")
        queryset = self.get_queryset().filter(bp_code=bp_code) if bp_code else self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
class OrderDetailView(generics.GenericAPIView):
    """
    - GET: Retrieve a Order by bp_code.
    - PUT: Update a Order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, order_no):
        """Helper method to get the object or return 404 using bp_code."""
        return get_object_or_404(Order, order_no=order_no)

    def get(self, request, order_no, *args, **kwargs):
        """Retrieve a Order by bp_code."""
        instance = self.get_object(order_no)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, order_no, *args, **kwargs):
        """Update an existing Order using bp_code."""
        instance = self.get_object(order_no)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def perform_create(self, serializer):
        """Automatically assign the logged-in user to the order"""
        serializer.save(user=self.request.user)  # Assign the authenticated user

    def create(self, request, *args, **kwargs):
        """Custom create method to ensure user authentication"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
        return super().create(request, *args, **kwargs)


class NewOrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

    def get_queryset(self):
        """Fetch only orders with status 'in-process'"""
        return Order.objects.filter(status="in-process").order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)



# class AssignOrdersToCraftsman(APIView):
#     def get(self, request):
#         """Return all orders and available craftsmen."""
#         orders = Order.objects.all()
#         craftsmen = ResUser.objects.filter(role_name='craftsman')

#         order_serializer = OrderCraftsmanSerializer(orders, many=True)
#         craftsman_serializer = CraftsmanSerializer(craftsmen, many=True)

#         return Response({
#             "orders": order_serializer.data,
#             "craftsmen": craftsman_serializer.data
#         })

#     def post(self, request):
#         """Manually assign selected orders to a craftsman."""
#         craftsman_id = request.data.get('craftsman_id')
#         order_ids = request.data.get('order_ids', [])

#         try:
#             craftsman = ResUser.objects.get(id=craftsman_id, role_name='craftsman')
#             orders = Order.objects.filter(id__in=order_ids)

#             if not orders.exists():
#                 return Response({"error": "No valid orders found"}, status=status.HTTP_400_BAD_REQUEST)

#             orders.update(craftsman=craftsman, state='assigned')
#             return Response({"message": "Orders assigned successfully!"}, status=status.HTTP_200_OK)

#         except ResUser.DoesNotExist:
#             return Response({"error": "Craftsman not found"}, status=status.HTTP_400_BAD_REQUEST)



class AssignOrdersToCraftsman(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return all new orders (in-process) and available craftsmen."""
        new_orders = Order.objects.filter(status="in-process")
        craftsmen = ResUser.objects.filter(role_name='craftsman')

        order_serializer = OrderCraftsmanSerializer(new_orders, many=True)
        craftsman_serializer = CraftsmanSerializer(craftsmen, many=True)

        return Response({
            "orders": order_serializer.data,
            "craftsmen": craftsman_serializer.data
        })

    def post(self, request):
        """Assign selected orders to a craftsman."""
        craftsman_id = request.data.get('craftsman_id')
        order_ids = request.data.get('order_ids', [])

        try:
            # Validate craftsman
            craftsman = ResUser.objects.get(id=craftsman_id, role_name='craftsman')

            # Validate orders
            orders = Order.objects.filter(id__in=order_ids, status="in-process")

            if not orders.exists():
                return Response({"error": "No valid orders found"}, status=status.HTTP_400_BAD_REQUEST)

            # Assign orders to craftsman and update status
            orders.update(craftsman=craftsman, status="assigned")

            return Response({"message": "Orders assigned successfully!"}, status=status.HTTP_200_OK)

        except ResUser.DoesNotExist:
            return Response({"error": "Craftsman not found"}, status=status.HTTP_400_BAD_REQUEST)


        
class OrderInProcessAPI(APIView):
    """API to view & update in-process orders."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        View all in-process orders.
        - Super Admin, Admin, and Craftsmen can view them.
        """
        if request.user.role_name in ['Super Admin', 'Admin', 'Craftsmen']:
            orders = Order.objects.filter(state='in-process')
            data = [
                {"id": order.id, "name": order.name, "reference_no": order.reference_no, "Craftsmen": order.craftsman.username if order.craftsman else None}
                for order in orders
            ]
            return Response({"in_process_orders": data}, status=status.HTTP_200_OK)

        return Response({"error": "You do not have permission to view orders."}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        """
        Craftsman updates order status to in-process.
        - Only craftsmen are allowed to update orders.
        """
        if request.user.role_name != 'Craftsmen':
            return Response({"error": "Only craftsmen can update orders."}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderStatusUpdateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            order = serializer.validated_data['order']
            order.state = 'in-process'
            order.save()
            return Response({"message": "Order is now in process.", "order_id": order.id, "state": order.state}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ApproveOrderView(generics.UpdateAPIView):
    """
    API View for craftsmen to mark orders as completed and for Admin/Super Admin to approve them.
    """
    serializer_class = ApproveOrderSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save()
            return Response({"message": f"Order {order.id} status updated to {order.state}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompletedOrdersView(generics.ListAPIView):
    """
    API View to list completed orders that have been approved.
    """
    serializer_class = CompletedOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(state="approved")
    
class RejectedOrdersView(generics.ListAPIView):
    """
    API to list all orders that were rejected by craftsmen.
    """
    serializer_class = OrderRejectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(state="rejected_by_craftsman")