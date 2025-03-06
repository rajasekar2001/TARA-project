from django.urls import path
from .views import BusinessPartnerView, BusinessPartnerDetailView, BusinessPartnerKYCView, BusinessPartnerDeleteView, BusinessPartnerKYCDetailView

urlpatterns = [
    path('BusinessPartner/create', BusinessPartnerView.as_view(), name='BusinessPartner-create'), 
    path('BusinessPartner/list', BusinessPartnerView.as_view(), name='BusinessPartner-list'), 
    path('BusinessPartner/detail/<str:bp_code>/', BusinessPartnerDetailView.as_view(), name='BusinessPartner-detail'), 
    path('BusinessPartner/delete/<str:bp_code>/', BusinessPartnerDeleteView.as_view(), name='BusinessPartner-delete'),
    path('BusinessPartner/revoke/<str:bp_code>/', BusinessPartnerDetailView.as_view(), {'action': 'revoke'}, name='BusinessPartner-revoke'),
    path('BusinessPartner/freeze/<str:bp_code>/', BusinessPartnerDetailView.as_view(), {'action': 'freeze'}, name='BusinessPartner-freeze'),

    # BusinessPartner KYC validation
    path('BusinessPartnerKYC/create', BusinessPartnerKYCView.as_view(), name='BusinessPartnerKYC-create'),
    path('BusinessPartnerKYC/list', BusinessPartnerKYCView.as_view(), name='BusinessPartnerKYC-list'),
    path('BusinessPartnerKYC/detail/<str:bp_code>/', BusinessPartnerKYCDetailView.as_view(), name='BusinessPartner-detail'), 

]
