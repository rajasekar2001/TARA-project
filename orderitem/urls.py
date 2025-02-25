from django.urls import path
from .views import OrderItemListView

urlpatterns = [
    path('order-item/list/', OrderItemListView.as_view(), name='order_item_list'),
    # path('order-item/update/<int:pk>/', OrderItemUpdateView.as_view(), name='order_item_update'),
    # path('order-item/delete/<int:pk>/', OrderItemDeleteView.as_view(), name='order_item_delete'),
]
