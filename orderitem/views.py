from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import OrderItem
from .serializers import OrderItemSerializer

class OrderItemListView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return queryset filtered by order number if provided, else all OrderItems.
        """
        order_no = self.request.query_params.get('order_no')
        if order_no:
            return OrderItem.objects.filter(order__order_no=order_no)
        return OrderItem.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to return serialized OrderItem data.
        """
        order_no = self.request.query_params.get('order_no')
        print(f"Received order_no: {order_no}")  # Debugging log

        queryset = self.get_queryset()

        if order_no and not queryset.exists():
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serialized_data = self.get_serializer(queryset, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

# Additional suggestion for get_all_order_details as a standalone function
# If required in your views.py, integrate this function for fetching order details.
def get_all_order_details():
    """
    Fetch all orders and their associated details.
    """
    try:
        orders = OrderItem.objects.select_related('order', 'order__product').all()

        order_list = []
        for order_item in orders:
            order = order_item.order
            order_details = {
                "Order No": order.order_no if order else None,
                "Status": order.status if order else None,
                "Due Date": order.due_date if order else None,
                "Narration": order.narration if order else None,
                "Product Details": {
                    "Product Name": order_item.product_name,
                    "Category": order_item.category,
                    "Price per Unit": order_item.price,
                    "Quantity": order_item.quantity,
                    "Total Price": order.price if order else None,
                },
            }
            order_list.append(order_details)

        return order_list
    except Exception as e:
        return {"error": str(e)}
