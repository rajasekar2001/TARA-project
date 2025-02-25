from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import RawMaterial, FinishedProduct, Production
from .serializers import RawMaterialSerializer, FinishedProductSerializer, ProductionSerializer


# Raw Material View (Single class handling all operations)
class RawMaterialView(generics.GenericAPIView):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            raw_material = get_object_or_404(self.queryset, pk=pk)
            serializer = self.serializer_class(raw_material)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        raw_material = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(raw_material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        raw_material = get_object_or_404(self.queryset, pk=pk)
        raw_material.delete()
        return Response({"message": "Raw Material deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Finished Product View (Single class handling all operations)
class FinishedProductView(generics.GenericAPIView):
    queryset = FinishedProduct.objects.all()
    serializer_class = FinishedProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            finished_product = get_object_or_404(self.queryset, pk=pk)
            serializer = self.serializer_class(finished_product)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        finished_product = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(finished_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        finished_product = get_object_or_404(self.queryset, pk=pk)
        finished_product.delete()
        return Response({"message": "Finished Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Production View (Single class handling all operations)
class ProductionView(generics.GenericAPIView):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            production = get_object_or_404(self.queryset, pk=pk)
            serializer = self.serializer_class(production)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        production = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(production, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        production = get_object_or_404(self.queryset, pk=pk)
        production.delete()
        return Response({"message": "Production entry deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
