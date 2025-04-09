from django.urls import path
from Admin.views import AdminRegistrationAPI, AdminDetailView, AdminDeleteView

urlpatterns = [
    # User API Endpoints
    path('Admin/registration/', AdminRegistrationAPI.as_view(), name='user_registration_api'),  # POST for user registration
    path('Admin/list/', AdminRegistrationAPI.as_view(), name='user_list_api'),  # GET for all users
    path('Admin/detail/<str:identifier>/', AdminDetailView.as_view(), name='user_detail_api'),  # GET for single user
    path('Admin/delete/<str:identifier>/', AdminDeleteView.as_view(), name='user_delete_api'),  # DELETE for deleting a user

]
    