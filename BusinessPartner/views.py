from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import BusinessPartner, BusinessPartnerKYC
from .serializers import BusinessPartnerSerializer, BusinessPartnerKYCSerializer


class BusinessPartnerView(generics.GenericAPIView):
    """
    API for BusinessPartner:
    - GET: Retrieve all Business Partners or filter by `bp_code`.
    - POST: Create a new Business Partner.
    """
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessPartnerSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get all Business Partners or filter by `bp_code`.
        """
        bp_code = request.query_params.get("bp_code")
        queryset = self.get_queryset().filter(bp_code=bp_code) if bp_code else self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new Business Partner.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessPartnerDetailView(generics.GenericAPIView):
    """
    API for a single Business Partner:
    - GET: Retrieve a Business Partner by ID.
    - PUT: Update a Business Partner.
    - DELETE: Delete a Business Partner.
    """
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessPartnerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Helper method to get the object or return 404."""
        return get_object_or_404(BusinessPartner, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        """Retrieve a Business Partner by ID (No POST form visible)."""
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """Update an existing Business Partner."""
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, *args, **kwargs):
    #     """Delete a Business Partner."""
    #     instance = self.get_object(pk)
    #     instance.delete()
    #     return Response({"message": "Business Partner deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    
class BusinessPartnerDeleteView(APIView):

    def delete(self, request, id, *args, **kwargs):
        user = get_object_or_404(BusinessPartner, id=id)
        user.delete()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(BusinessPartner, id=id)
        user.delete()
        return Response({"detail": "User deleted successfully using GET request"}, status=status.HTTP_200_OK)

class BusinessPartnerKYCView(generics.GenericAPIView):
    """
    API for BusinessPartnerKYC:
    - GET: Retrieve all KYC entries or filter by `bp_code`.
    - POST: Create a new KYC entry.
    """
    queryset = BusinessPartnerKYC.objects.all()
    serializer_class = BusinessPartnerKYCSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieve Business Partner KYC details or filter by `bp_code`."""
        bp_code = request.query_params.get("bp_code")
        queryset = self.get_queryset().filter(bp_code=bp_code) if bp_code else self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Create a new BusinessPartnerKYC entry."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessPartnerKYCDetailView(generics.GenericAPIView):
    """
    API for a single Business Partner KYC:
    - GET: Retrieve a KYC entry by ID.
    - PUT: Update a KYC entry.
    - DELETE: Delete a KYC entry.
    """
    queryset = BusinessPartnerKYC.objects.all()
    serializer_class = BusinessPartnerKYCSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Helper method to get the object or return 404."""
        return get_object_or_404(BusinessPartnerKYC, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        """Retrieve a Business Partner KYC entry."""
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """Update an existing Business Partner KYC entry."""
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """Delete a Business Partner KYC entry."""
        instance = self.get_object(pk)
        instance.delete()
        return Response({"message": "Business Partner KYC deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
