from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from Admin.models import Admin
from Admin.serializers import AdminSerializer
from rest_framework.permissions import AllowAny
import random

class AdminRegistrationAPI(generics.GenericAPIView):
    """
    API View for Admin registration.
    """
    serializer_class = AdminSerializer
    permission_classes = [AllowAny]
    queryset = Admin.objects.all()

    def post(self, request):
        """
        Create a Admin.
        """
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Debugging

        email_id = serializer.validated_data.get('email_id')  # Safe get
        mobile_no = serializer.validated_data.get('mobile_no')

        # Check for duplicate email and mobile number
        if email_id and Admin.objects.filter(email_id=email_id).exists():
            return Response({"error": "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)
        if mobile_no and Admin.objects.filter(mobile_no=mobile_no).exists():
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
            user = get_object_or_404(Admin, id=id)
            serializer = self.serializer_class(user)
        else:
            users = Admin.objects.all()
            serializer = self.serializer_class(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminDetailView(generics.GenericAPIView):
    """
    API for a single Admin:
    - GET: Retrieve a Admin by email or mobile_no.
    - PUT: Update a Admin.
    """
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def get_object(self, identifier):
        """Helper method to get the object by email or mobile_no or return 404."""
        # First try to find by email
        try:
            return Admin.objects.get(email_id=identifier)
        except Admin.DoesNotExist:
            try:
                # If not found by email, try by mobile_no
                return Admin.objects.get(mobile_no=identifier)
            except Admin.DoesNotExist:
                raise Http404("No Admin matches the given query.")

    def get(self, request, identifier, *args, **kwargs):
        """Retrieve a Admin by email or mobile_no."""
        instance = self.get_object(identifier)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, identifier, *args, **kwargs):
        """Update an existing Admin using email or mobile_no."""
        instance = self.get_object(identifier)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDeleteView(generics.GenericAPIView):
    """
    API for deleting a Admin:
    - DELETE: Delete a Admin by email or mobile_no
    """
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def get_object(self, identifier):
        """Helper method to get the object by email or mobile_no or return 404."""
        try:
            return Admin.objects.get(email=identifier)
        except Admin.DoesNotExist:
            try:
                return Admin.objects.get(mobile_no=identifier)
            except Admin.DoesNotExist:
                raise Http404("No Admin matches the given query.")
            

    def delete(self, request, identifier, *args, **kwargs):
        """Delete a Admin by email or mobile_no."""
        instance = self.get_object(identifier)
        instance.delete()
        return Response(
            {
                "status": "success",
                "message": "Admin deleted successfully",
            },
            status=status.HTTP_200_OK
        )
