import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from .models import Customer
from .serializers import CustomerSerializer


class CustomerListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        customers = Customer.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10

        try:
            paginated_customers = paginator.paginate_queryset(customers, request)
            serializer = CustomerSerializer(
                paginated_customers, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(serializer.data)
        except Exception:
            return Response(
                {"error": "Invalid page request"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            if 'photo' in request.FILES:
                if request.FILES['photo'].size > 10 * 1024 * 1024:
                    return Response(
                        {"error": "File size exceeds 10MB limit"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = CustomerSerializer(
                data=request.data,
                context={"request": request}
            )

            if serializer.is_valid():
                customer = serializer.save(user=request.user)

                if customer.photo:
                    print(f"✔️ File saved to: {customer.photo.path}")
                    print(f"✔️ Accessible at: {request.build_absolute_uri(customer.photo.url)}")

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk, user=request.user)
            serializer = CustomerSerializer(customer, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(
                {'detail': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk, user=request.user)

            serializer = CustomerSerializer(
                customer,
                data=request.data,
                partial=True,  # allows partial update
                context={"request": request}
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Customer.DoesNotExist:
            return Response(
                {'detail': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        return self.put(request, pk)  # alias for partial update


def health_check(request):
    return JsonResponse({"status": "ok"})
