from django.urls import path
from Users.views import UsersRegistrationAPI, UsersDetailView, UsersDeleteView

urlpatterns = [
    # User API Endpoints
    path('Users/registration/', UsersRegistrationAPI.as_view(), name='user_registration_api'),  # POST for user registration
    path('Users/list/', UsersRegistrationAPI.as_view(), name='user_list_api'),  # GET for all users
    path('Users/detail/<str:identifier>/', UsersDetailView.as_view(), name='user_detail_api'),  # GET for single user
    path('Users/delete/<str:identifier>/', UsersDeleteView.as_view(), name='user_delete_api'),  # DELETE for deleting a user

]
    