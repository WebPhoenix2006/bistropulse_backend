from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Customer
from .serializers import CustomerSerializer

class CustomerListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        customers = Customer.objects.filter(user=request.user)
        serializer = CustomerSerializer(customers, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
