from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from Craftsman.models import Craftman
from Craftsman.serializers import CraftmanSerializer
from rest_framework.permissions import AllowAny
import random

class CraftsmanRegistrationAPI(generics.GenericAPIView):
    """
    API View for Craftsman registration.
    """
    serializer_class = CraftmanSerializer
    permission_classes = [AllowAny]
    queryset = Craftman.objects.all()

    def post(self, request):
        """
        Create a new Craftsman.
        """
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Debugging

        email_id = serializer.validated_data.get('email_id')  # Safe get
        mobile_no = serializer.validated_data.get('mobile_no')

        # Check for duplicate email and mobile number
        if email_id and Craftman.objects.filter(email_id=email_id).exists():
            return Response({"error": "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)
        if mobile_no and Craftman.objects.filter(mobile_no=mobile_no).exists():
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
            user = get_object_or_404(Craftman, id=id)
            serializer = self.serializer_class(user)
        else:
            users = Craftman.objects.all()
            serializer = self.serializer_class(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class CraftsmanDetailView(generics.GenericAPIView):
    """
    API for a single Craftsman:
    - GET: Retrieve a Craftsman by email or mobile_no.
    - PUT: Update a Craftsman.
    """
    queryset = Craftman.objects.all()
    serializer_class = CraftmanSerializer

    def get_object(self, identifier):
        """Helper method to get the object by email or mobile_no or return 404."""
        # First try to find by email
        try:
            return Craftman.objects.get(email_id=identifier)
        except Craftman.DoesNotExist:
            try:
                # If not found by email, try by mobile_no
                return Craftman.objects.get(mobile_no=identifier)
            except Craftman.DoesNotExist:
                raise Http404("No Craftsman matches the given query.")

    def get(self, request, identifier, *args, **kwargs):
        """Retrieve a Craftsman by email or mobile_no."""
        instance = self.get_object(identifier)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, identifier, *args, **kwargs):
        """Update an existing Craftsman using email or mobile_no."""
        instance = self.get_object(identifier)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CraftsmanDeleteView(generics.GenericAPIView):
    """
    API for deleting a Craftsman:
    - DELETE: Delete a Craftsman by email or mobile_no
    """
    queryset = Craftman.objects.all()
    serializer_class = CraftmanSerializer

    def get_object(self, identifier):
        """Helper method to get the object by email or mobile_no or return 404."""
        try:
            return Craftman.objects.get(email=identifier)
        except Craftman.DoesNotExist:
            try:
                return Craftman.objects.get(mobile_no=identifier)
            except Craftman.DoesNotExist:
                raise Http404("No Craftsman matches the given query.")
            

    def delete(self, request, identifier, *args, **kwargs):
        """Delete a Craftsman by email or mobile_no."""
        instance = self.get_object(identifier)
        instance.delete()
        return Response(
            {
                "status": "success",
                "message": "Craftsman deleted successfully",
            },
            status=status.HTTP_200_OK
        )

