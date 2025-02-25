from django.urls import path
from .views import RawMaterialView, FinishedProductView, ProductionView

urlpatterns = [
    # Raw Material URLs
    path('raw-materials/', RawMaterialView.as_view(), name='raw-material-list'),
    path('raw-materials/create/', RawMaterialView.as_view(), name='raw-material-create'),
    path('raw-materials/<int:pk>/', RawMaterialView.as_view(), name='raw-material-detail'),
    path('raw-materials/<int:pk>/delete/', RawMaterialView.as_view(), name='raw-material-delete'),

    # Finished Product URLs
    path('finished-products/', FinishedProductView.as_view(), name='finished-product-list'),
    path('finished-products/create/', FinishedProductView.as_view(), name='finished-product-create'),
    path('finished-products/<int:pk>/', FinishedProductView.as_view(), name='finished-product-detail'),
    path('finished-products/<int:pk>/delete/', FinishedProductView.as_view(), name='finished-product-delete'),

    # Production URLs
    path('production/', ProductionView.as_view(), name='production-list'),
    path('production/create/', ProductionView.as_view(), name='production-create'),
    path('production/<int:pk>/', ProductionView.as_view(), name='production-detail'),
    path('production/<int:pk>/delete/', ProductionView.as_view(), name='production-delete'),
]
