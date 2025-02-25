from django.urls import path
from .views import BusinessPartnerView, BusinessPartnerDetailView, BusinessPartnerKYCView

urlpatterns = [
    path('BusinessPartner/create', BusinessPartnerView.as_view(), name='BusinessPartner-create'), # Handles POST (create)
    path('BusinessPartner/list', BusinessPartnerView.as_view(), name='BusinessPartner-list'),  # Handles GET (list)
    path('BusinessPartner/detail/<int:pk>/', BusinessPartnerDetailView.as_view(), name='BusinessPartner-detail'),  # Fix: Use correct view
    path('BusinessPartner/delete/<int:pk>/', BusinessPartnerDetailView.as_view(), name='BusinessPartner-delete'),  # Fix: Use correct view

    # BusinessPartner KYC validation
    path('BusinessPartnerKYC/create', BusinessPartnerKYCView.as_view(), name='BusinessPartnerKYC-create'),
    path('BusinessPartnerKYC/list', BusinessPartnerKYCView.as_view(), name='BusinessPartnerKYC-list'),
]
