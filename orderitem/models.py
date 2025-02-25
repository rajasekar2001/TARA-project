from django.db import models
from order.models import Order


# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Order", null=True)  # Link to Order model
    product_name = models.CharField(max_length=255, verbose_name="product_name")
    quantity = models.PositiveIntegerField(default=1, verbose_name="quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="price")
    category = models.CharField(max_length=255, blank=True, null=True, verbose_name="category")
    
    @property
    def order_no(self):
        """Fetch order number directly from the associated order."""
        return self.order.order_no if self.order else None

    @property
    def product_name(self):
        """Fetch product name directly from the associated order."""
        return self.order.product.name if self.order and self.order.product else None

    @property
    def quantity(self):
        """Fetch quantity directly from the associated order."""
        return self.order.quantity if self.order else None

    @property
    def price(self):
        """Fetch price directly from the associated order."""
        return self.order.price if self.order else None

    @property
    def category(self):
        """Fetch category directly from the associated order."""
        return self.order.category if self.order else None

    @property
    def order_status(self):
        """Fetch order status directly from the associated order."""
        return self.order.status if self.order else None

    def __str__(self):
        product_name = self.product_name if self.product_name else "Unknown Product"
        return f"{self.quantity} x {product_name} (Order: {self.order_no})"


# Fetch All Order Details
def get_all_order_details():
    """
    Fetch all orders and their associated details.
    """
    try:
        # Fetch all orders
        orders = Order.objects.select_related('product').all()

        order_list = []
        for order in orders:
            order_details = {
                "Order No": order.order_no,
                "Status": order.status,
                "Due Date": order.due_date,
                "Narration": order.narration,
                "Product Details": {
                    "Product Name": order.product.name if order.product else None,
                    "Category": order.category,
                    "Price per Unit": order.product.price if order.product else None,
                    "Quantity": order.quantity,
                    "Total Price": order.price,
                },
            }
            order_list.append(order_details)

        return order_list
    except Exception as e:
        return {"error": str(e)}
