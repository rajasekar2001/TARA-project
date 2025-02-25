from django.urls import path
from .views import ProductAPI, ProductImageAPI

urlpatterns = [
    path('product/create/', ProductAPI.as_view(), name='product_create_api'),
    path('product/update/<int:id>/', ProductAPI.as_view(), name='product_update_api'),
    path('product/delete/<int:id>/', ProductAPI.as_view(), name='product_delete_api'),
    path('product/list/', ProductAPI.as_view(), name='product_list_api'),
    path('product/detail/<int:id>/', ProductAPI.as_view(), name='product_detail_api'),
    # product image
    path('product/image/',ProductImageAPI.as_view(), name='add_product_image'),
    path('product/image/update/<int:id>/', ProductImageAPI.as_view(), name='product_update_api'),
    path('product/image/delete/<int:id>/', ProductImageAPI.as_view(), name='product_delete_api'),
    path('product/image/list/', ProductImageAPI.as_view(), name='product_list_api'),
    path('product/image/detail/<int:id>/', ProductImageAPI.as_view(), name='product_detail_api'),
]
