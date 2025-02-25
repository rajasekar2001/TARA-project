from django.urls import path
from user.views import ResUserRegistrationAPI, ResAdminAPI, LoginAPIView, UserUpdateView, UserDeleteView, AdminUpdateView, AdminDeleteView

urlpatterns = [
    # User API Endpoints
    path('user/registration/', ResUserRegistrationAPI.as_view(), name='user_registration_api'),  # POST for user registration
    path('user/update/<int:id>/', UserUpdateView.as_view(), name='user_update_api'),  # PUT for updating a user
    path('user/delete/<int:id>/', UserDeleteView.as_view(), name='user_delete_api'),  # DELETE for deleting a user
    path('user/list/', ResUserRegistrationAPI.as_view(), name='user_list_api'),  # GET for all users
    path('user/detail/<int:id>/', ResUserRegistrationAPI.as_view(), name='user_detail_api'),  # GET for single user

    # Admin API Endpoints
    path('admin/registration/', ResAdminAPI.as_view(), name='admin_registration_api'),  # POST for admin registration
    path('admin/update/<int:id>/', AdminUpdateView.as_view(), name='admin_update_api'),  # PUT for updating an admin
    path('admin/delete/<int:id>/', AdminDeleteView.as_view(), name='admin_delete_api'),  # DELETE for deleting an admin
    path('admin/list/', ResAdminAPI.as_view(), name='admin_list_api'),  # GET for all admins
    path('admin/detail/<int:id>/', ResAdminAPI.as_view(), name='admin_detail_api'),  # GET for single admin

    # # permission group API Endpoints
    # path('respermissiongroup/create/', PermissionGroupAPI.as_view(), name='permission_group'), # Post for permission group creation
    # path('respermissiongroup/update/<int:id>/', PermissionGroupAPI.as_view(), name='permission_group_update'), # PUT for updateing permission group
    # path('respermissiongroup/delete/<int:id>/', PermissionGroupAPI.as_view(), name='permission_group_delete'), # DELETE for deleting permission group
    # path('respermissiongroup/list/', PermissionGroupAPI.as_view(), name='permission_group_list'), # GET for all permission groups
    # path('respermissiongroup/detail/<int:id>/', PermissionGroupAPI.as_view(), name='permission_group_details'), # GET for single permission group

    # Login API Endpoint
    path('reslogin/', LoginAPIView.as_view(), name='login') # POST for user login
]
    