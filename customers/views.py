from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.pagination import PageNumberPagination

from rest_framework.parsers import MultiPartParser, FormParser

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

            # ✅ Ensure the customer now has a file
            print("✔️ File saved at:", customer.photo)

            # Re-serialize AFTER saving
            response_serializer = CustomerSerializer(customer, context={"request": request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


