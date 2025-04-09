from django.urls import path
from Craftsman.views import CraftsmanRegistrationAPI, CraftsmanDetailView, CraftsmanDeleteView

urlpatterns = [
    # User API Endpoints
    path('Craftsman/registration/', CraftsmanRegistrationAPI.as_view(), name='user_registration_api'),  # POST for user registration
    path('Craftsman/list/', CraftsmanRegistrationAPI.as_view(), name='user_list_api'),  # GET for all users
    path('Craftsman/detail/<str:identifier>/', CraftsmanDetailView.as_view(), name='user_detail_api'),  # GET for single user
    path('Craftsman/delete/<str:identifier>/', CraftsmanDeleteView.as_view(), name='user_delete_api'),  # DELETE for deleting a user

]
    