from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from SuperAdmin.models import SuperAdmin
from SuperAdmin.serializers import SuperAdminSerializer
from rest_framework.permissions import AllowAny
import random

class SuperAdminRegistrationAPI(generics.GenericAPIView):
    """
    API View for SuperAdmin registration.
    """
    serializer_class = SuperAdminSerializer
    permission_classes = [AllowAny]
    queryset = SuperAdmin.objects.all()

    def post(self, request):
        """
        Create a new SuperAdmin.
        """
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Debugging

        email_id = serializer.validated_data.get('email_id')  # Safe get
        mobile_no = serializer.validated_data.get('mobile_no')

        # Check for duplicate email and mobile number
        if email_id and SuperAdmin.objects.filter(email_id=email_id).exists():
            return Response({"error": "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)
        if mobile_no and SuperAdmin.objects.filter(mobile_no=mobile_no).exists():
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
            user = get_object_or_404(SuperAdmin, id=id)
            serializer = self.serializer_class(user)
        else:
            users = SuperAdmin.objects.all()
            serializer = self.serializer_class(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class SuperAdminDetailView(generics.GenericAPIView):
    """
    API for a single SuperAdmin:
    - GET: Retrieve a SuperAdmin by email or mobile_no.
    - PUT: Update a SuperAdmin.
    """
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer

    def get_object(self, identifier):
        """Helper method to get the object by email or mobile_no or return 404."""
        # First try to find by email
        try:
            return SuperAdmin.objects.get(email_id=identifier)
        except SuperAdmin.DoesNotExist:
            try:
                # If not found by email, try by mobile_no
                return SuperAdmin.objects.get(mobile_no=identifier)
            except SuperAdmin.DoesNotExist:
                raise Http404("No SuperAdmin matches the given query.")

    def get(self, request, identifier, *args, **kwargs):
        """Retrieve a SuperAdmin by email or mobile_no."""
        instance = self.get_object(identifier)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, identifier, *args, **kwargs):
        """Update an existing SuperAdmin using email or mobile_no."""
        instance = self.get_object(identifier)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuperAdminDeleteView(generics.GenericAPIView):
    """
    API for deleting a SuperAdmin:
    - DELETE: Delete a SuperAdmin by email or mobile_no
    """
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer

    def get_object(self, identifier):
        """Helper method to get the object by email or mobile_no or return 404."""
        try:
            return SuperAdmin.objects.get(email=identifier)
        except SuperAdmin.DoesNotExist:
            try:
                return SuperAdmin.objects.get(mobile_no=identifier)
            except SuperAdmin.DoesNotExist:
                raise Http404("No SuperAdmin matches the given query.")
            

    def delete(self, request, identifier, *args, **kwargs):
        """Delete a SuperAdmin by email or mobile_no."""
        instance = self.get_object(identifier)
        instance.delete()
        return Response(
            {
                "status": "success",
                "message": "SuperAdmin deleted successfully",
            },
            status=status.HTTP_200_OK
        )
