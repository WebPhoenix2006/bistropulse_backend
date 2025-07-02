import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse


class CustomerListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Allow file upload

    def get(self, request):
        customers = Customer.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        paginated_customers = paginator.paginate_queryset(customers, request)
        serializer = CustomerSerializer(paginated_customers, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            customer = serializer.save(user=request.user)
            
            # Debugging prints
            if customer.photo:  # Check if photo exists
                print("✔️ File saved at:", customer.photo.path)
                print("✔️ File exists:", os.path.exists(customer.photo.path))
                print("✔️ File URL:", customer.photo.url)
                print("✔️ Absolute URL:", request.build_absolute_uri(customer.photo.url))
            else:
                print("⚠️ No photo was saved")
            
            # Return the serialized data with photo_url
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk, user=request.user)
            serializer = CustomerSerializer(customer, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'detail': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        

def health_check(request):
    return JsonResponse({"status": "ok"})