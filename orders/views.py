from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .serilalizers import OrderSerializer
from .models import Order
from restaurants.models import Rider  # or wherever your Rider model lives


class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET: 
        - Admin: See all orders
        - Manager: See orders for their restaurant
        - Rider: See only their own orders
    POST: 
        - Manager only: Create order under their restaurant
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Order.objects.all().order_by('-created_at')

        elif user.role == 'manager':
            if not hasattr(user, 'restaurant'):
                raise PermissionDenied("Manager is not associated with any restaurant.")
            return Order.objects.filter(restaurant=user.restaurant).order_by('-created_at')

        elif user.role == 'rider':
            # Get the rider instance that matches the current user
            rider = get_object_or_404(Rider, user=user)
            return Order.objects.filter(rider=rider).order_by('-created_at')

        return Order.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'manager':
            if not hasattr(user, 'restaurant'):
                raise PermissionDenied("Manager is not associated with any restaurant.")
            serializer.save(restaurant=user.restaurant)

        else:
            raise PermissionDenied("Only managers can create orders.")


class RiderOrderListView(generics.ListAPIView):
    """
    Admin or Manager can view a specific rider's orders.
    Admin: Access all riders
    Manager: Only their restaurant's riders
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        rider_id = self.kwargs.get('rider_id')

        rider = get_object_or_404(Rider, id=rider_id)

        if user.role == 'admin':
            # Admin can access any rider
            return Order.objects.filter(rider=rider).order_by('-created_at')

        elif user.role == 'manager':
            if not hasattr(user, 'restaurant'):
                raise PermissionDenied("Manager is not associated with any restaurant.")

            if rider.restaurant != user.restaurant:
                raise PermissionDenied("This rider does not belong to your restaurant.")

            return Order.objects.filter(rider=rider).order_by('-created_at')

        else:
            raise PermissionDenied("You do not have permission to view this rider's orders.")
