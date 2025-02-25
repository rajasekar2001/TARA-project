from django.urls import path
from .views import OrderAPI,SallerFetchOrderAPI,AssignToCraftsmanSallerUpdateOrderAPI,AssignToBackSellerOrderAPI

urlpatterns = [
    path('orders/create', OrderAPI.as_view(), name='order-create'), # Handles POST (create)
    path('orders/list', OrderAPI.as_view(), name='order-list'),  # Handles GET (list)
    path('orders/detail', OrderAPI.as_view(), name='order-detail'),
    path('orders/delete/<int:id>/', OrderAPI.as_view(), name='update-delete'),  # Handles GET, PUT, DELETE for a specific order
    path('orders/seller', SallerFetchOrderAPI.as_view(), name='seller-orders'),  # Handles GET for seller
    path('seller/update/<int:orderid>/', AssignToCraftsmanSallerUpdateOrderAPI.as_view(), name='seller-orders-update'),  # Handles GET for seller
    path('craftsman/update/<int:orderid>/', AssignToBackSellerOrderAPI.as_view(), name='craftsman-orders-update'),  # Handles GET for seller
]
