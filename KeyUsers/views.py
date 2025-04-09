from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from KeyUsers.models import KeyUsers
from KeyUsers.serializers import KeyUserSerializer
from rest_framework.permissions import AllowAny
import random


class KeyUsersRegistrationAPI(generics.GenericAPIView):
    """
    API View for KeyUsers registration.
    """
    serializer_class = KeyUserSerializer
    permission_classes = [AllowAny]
    queryset = KeyUsers.objects.all()

    def post(self, request):
        """
        Create a new KeyUsers.
        """
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Debugging

        email_id = serializer.validated_data.get('email_id')  # Safe get
        mobile_no = serializer.validated_data.get('mobile_no')

        # Check for duplicate email and mobile number
        if email_id and KeyUsers.objects.filter(email_id=email_id).exists():
            return Response({"error": "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)
        if mobile_no and KeyUsers.objects.filter(mobile_no=mobile_no).exists():
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
            user = get_object_or_404(KeyUsers, id=id)
            serializer = self.serializer_class(user)
        else:
            users = KeyUsers.objects.all()
            serializer = self.serializer_class(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class KeyUsersDetailView(generics.GenericAPIView):
    """
    API for a single KeyUsers:
    - GET: Retrieve a KeyUsers by email or mobile_no.
    - PUT: Update a KeyUsers.
    """
    queryset = KeyUsers.objects.all()
    serializer_class = KeyUserSerializer

    def get_object(self, identifier):
        """Helper method to get the object by email or mobile_no or return 404."""
        # First try to find by email
        try:
            return KeyUsers.objects.get(email_id=identifier)
        except KeyUsers.DoesNotExist:
            try:
                # If not found by email, try by mobile_no
                return KeyUsers.objects.get(mobile_no=identifier)
            except KeyUsers.DoesNotExist:
                raise Http404("No KeyUsers matches the given query.")

    def get(self, request, identifier, *args, **kwargs):
        """Retrieve a KeyUsers by email or mobile_no."""
        instance = self.get_object(identifier)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, identifier, *args, **kwargs):
        """Update an existing KeyUsers using email or mobile_no."""
        instance = self.get_object(identifier)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KeyUsersDeleteView(generics.GenericAPIView):
    """
    API for deleting a KeyUsersr:
    - DELETE: Delete a KeyUsers by email or mobile_no
    """
    queryset = KeyUsers.objects.all()
    serializer_class = KeyUserSerializer

    def get_object(self, identifier):
        """Helper method to get the object by email or mobile_no or return 404."""
        try:
            return KeyUsers.objects.get(email=identifier)
        except KeyUsers.DoesNotExist:
            try:
                return KeyUsers.objects.get(mobile_no=identifier)
            except KeyUsers.DoesNotExist:
                raise Http404("No KeyUsers matches the given query.")
            

    def delete(self, request, identifier, *args, **kwargs):
        """Delete a KeyUsers by email or mobile_no."""
        instance = self.get_object(identifier)
        instance.delete()
        return Response(
            {
                "status": "success",
                "message": "KeyUsers deleted successfully",
            },
            status=status.HTTP_200_OK
        )
