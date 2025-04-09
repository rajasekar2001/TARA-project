from django.urls import path
from KeyUsers.views import KeyUsersRegistrationAPI, KeyUsersDetailView, KeyUsersDeleteView

urlpatterns = [
    # User API Endpoints
    path('KeyUsers/registration/', KeyUsersRegistrationAPI.as_view(), name='user_registration_api'),  # POST for user registration
    path('KeyUsers/list/', KeyUsersRegistrationAPI.as_view(), name='user_list_api'),  # GET for all users
    path('KeyUsers/detail/<str:identifier>/', KeyUsersDetailView.as_view(), name='user_detail_api'),  # GET for single user
    path('KeyUsers/delete/<str:identifier>/', KeyUsersDeleteView.as_view(), name='user_delete_api'),  # DELETE for deleting a user

]
    