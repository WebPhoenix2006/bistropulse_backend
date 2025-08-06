from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .serilalizers import OrderSerializer
from .models import Order
from restaurants.models import Rider  # or wherever your Rider model lives


class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET: List all orders belonging to the authenticated user's restaurant.
    POST: Create a new order under the authenticated user's restaurant.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'restaurant'):
            return Order.objects.filter(restaurant=user.restaurant).order_by('-created_at')
        
        return Order.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if hasattr(user, 'restaurant'):
            serializer.save(restaurant=user.restaurant)
        else:
            raise PermissionDenied("You are not associated with any restaurant.")


class RiderOrderListView(generics.ListAPIView):
    """
    GET: List all orders assigned to a specific rider (admin view).
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        rider_id = self.kwargs.get('rider_id')


        # Check if the rider exists and is part of the admin's restaurant
        rider = get_object_or_404(Rider, id=rider_id, restaurant=user.restaurant)

        return Order.objects.filter(restaurant=user.restaurant, rider=rider).order_by('-created_at')
