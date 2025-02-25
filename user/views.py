from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from user.models import ResUser, RoleDashboardMapping
from user.serializers import ResUserSerializer, ResAdminUserSerializer, LoginSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random
from rest_framework.views import APIView


class ResUserRegistrationAPI(generics.GenericAPIView):
    """
    API View for user registration.
    """
    serializer_class = ResUserSerializer
    queryset = ResUser.objects.all()

    def post(self, request):
        """
        Create a new user.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check for duplicate email and mobile number
        if ResUser.objects.filter(email_id=serializer.validated_data['email_id']).exists():
            return Response({"error": "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)
        if ResUser.objects.filter(mobile_no=serializer.validated_data['mobile_no']).exists():
            return Response({"error": "Mobile number is already taken"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a unique username
        username = f"User{random.randint(1000, 9999)}"
        user = serializer.save(username=username)
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
    
    def get(self, request, id=None):
        """
        Retrieve user(s).
        """ 
        if id:
            user = get_object_or_404(ResUser, id=id)
            serializer = self.serializer_class(user)
        else:
            users = ResUser.objects.all()
            serializer = self.serializer_class(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    serializer_class = ResUserSerializer

    def get(self, request, id, *args, **kwargs):
        """Retrieve user data for the update form."""
        user = get_object_or_404(ResUser, id=id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        """Update user details."""
        user = get_object_or_404(ResUser, id=id)
        serializer = self.serializer_class(instance=user, data=request.data, partial=True)  # Partial update

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UserDeleteView(APIView):

    def delete(self, request, id, *args, **kwargs):
        user = get_object_or_404(ResUser, id=id)
        user.delete()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(ResUser, id=id)
        user.delete()
        return Response({"detail": "User deleted successfully using GET request"}, status=status.HTTP_200_OK)



class ResAdminAPI(generics.GenericAPIView):
    """
    API View for admin registration and management.
    """
    serializer_class = ResAdminUserSerializer
    queryset = ResUser.objects.all()
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Create a new admin.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check for duplicate email and mobile number
        if ResUser.objects.filter(email_id=serializer.validated_data['email_id']).exists():
            return Response({"error": "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)
        if ResUser.objects.filter(mobile_no=serializer.validated_data['mobile_no']).exists():
            return Response({"error": "Mobile number is already taken"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the admin using serializer
        admin = serializer.save()

        return Response(self.serializer_class(admin).data, status=status.HTTP_201_CREATED)

    # def get(self, request, id=None):
    #     """
    #     Retrieve admin(s).
    #     """
    #     if id:
    #         admin = get_object_or_404(ResUser, id=id)
    #     else:
    #         admins = ResUser.objects.filter(role_name='admin')
        
    #     serializer = self.serializer_class(admins if not id else admin, many=not id)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request, id=None):
        """
        Retrieve admin(s).
        """
        if id:
            admin = get_object_or_404(ResUser, id=id)
            serializer = self.serializer_class(admin)
        else:
            admin = ResUser.objects.all()
            serializer = self.serializer_class(admin, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def put(self, request, id):
    #     """
    #     Update admin details.
    #     """
    #     admin = get_object_or_404(ResUser, id=id)
    #     serializer = self.serializer_class(admin, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class AdminUpdateView(APIView):
    serializer_class = ResUserSerializer

    def get(self, request, id, *args, **kwargs):
        """Retrieve admin data for the update form."""
        admin = get_object_or_404(ResUser, id=id)
        serializer = self.serializer_class(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        """Update admin details."""
        admin = get_object_or_404(ResUser, id=id)
        serializer = self.serializer_class(instance=admin, data=request.data, partial=True)  # Partial update

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, id):
    #     """
    #     Delete a user.
    #     """
    #     user = ResUser.objects.filter(id=id).first()
        
    #     if not user:
    #         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    #     user.delete()
    #     return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class AdminDeleteView(APIView):

    def delete(self, request, id, *args, **kwargs):
        admin = get_object_or_404(ResUser, id=id)
        admin.delete()
        return Response({"detail": "Admin deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    def get(self, request, id, *args, **kwargs):
        admin = get_object_or_404(ResUser, id=id)
        admin.delete()
        return Response({"detail": "Admin deleted successfully using GET request"}, status=status.HTTP_200_OK)




def get_dashboard_url(role):
    try:
        mapping = RoleDashboardMapping.objects.get(role=role)
        return mapping.dashboard_url
    except RoleDashboardMapping.DoesNotExist:
        return None  # Default behavior if no mapping exists

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_or_mobile = serializer.validated_data.get('email_or_mobile')
        password = serializer.validated_data.get('password')

        try:
            # Check if input is email or mobile number
            if '@' in email_or_mobile:  # If it's an email
                current_user = ResUser.objects.get(email_id=email_or_mobile)
            else:  # If it's a mobile number
                current_user = ResUser.objects.get(mobile_no=email_or_mobile)

        except ResUser.DoesNotExist:
            return Response({"error": "This email or mobile number is not registered."}, status=status.HTTP_404_NOT_FOUND)

        if not current_user.check_password(password):
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        if current_user.status != 'active':
            return Response({"error": "This account is inactive."}, status=status.HTTP_403_FORBIDDEN)

        # Ensure Role-Dashboard Mapping Exists
        dashboard_url = get_dashboard_url(current_user.role_name) or "/default-dashboard/"

        # Safe Permission Fetching
        try:
            user_permissions = current_user.user_permissions.all()
            permission_names = [perm.codename for perm in user_permissions]
        except Exception as e:
            permission_names = []
            print(f"Warning: Could not fetch permissions - {e}")

        return Response({
            'msg': f'Login successful! Welcome, {current_user.full_name}',
            'user_id': current_user.id,
            'user_code':current_user.user_code,
            'role_name': current_user.role_name,
            'status': current_user.status,
            'dashboard': dashboard_url,
            'permissions': permission_names
        }, status=status.HTTP_200_OK)
