from django.urls import path
from SuperAdmin.views import SuperAdminRegistrationAPI, SuperAdminDetailView, SuperAdminDeleteView

urlpatterns = [
    # User API Endpoints
    path('SuperAdmin/registration/', SuperAdminRegistrationAPI.as_view(), name='user_registration_api'),  # POST for user registration
    path('SuperAdmin/list/', SuperAdminRegistrationAPI.as_view(), name='user_list_api'),  # GET for all users
    path('SuperAdmin/detail/<str:identifier>/', SuperAdminDetailView.as_view(), name='user_detail_api'),  # GET for single user
    path('SuperAdmin/delete/<str:identifier>/', SuperAdminDeleteView.as_view(), name='user_delete_api'),  # DELETE for deleting a user

]
    