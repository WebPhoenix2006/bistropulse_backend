from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .serilalizers import OrderSerializer
from .models import Order
from restaurants.models import Restaurant, Rider  # Adjust if located elsewhere


# ===========================
# List + Create Orders (General)
# ===========================
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

        if user.role == "admin":
            return Order.objects.all().order_by("-date_ordered")
        elif user.role == "manager":
            if not hasattr(user, "restaurant"):
                raise PermissionDenied("Manager is not associated with any restaurant.")
            return Order.objects.filter(restaurant=user.restaurant).order_by(
                "-date_ordered"
            )
        elif user.role == "rider":
            rider = get_object_or_404(Rider, user=user)
            return Order.objects.filter(rider=rider).order_by("-date_ordered")

        return Order.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role in ["manager", "admin"]:
            branch = serializer.validated_data.get("branch")
            restaurant = serializer.validated_data.get("restaurant")

            if user.role == "manager":
                # Managers should only link to their own restaurant/branch
                if hasattr(user, "restaurant") and not restaurant:
                    restaurant = user.restaurant
                elif hasattr(user, "branch") and not branch:
                    branch = user.branch
                else:
                    raise PermissionDenied(
                        "Manager is not linked to any restaurant or branch."
                    )

            serializer.save(branch=branch, restaurant=restaurant)

        else:
            raise PermissionDenied("Only managers or admins can create orders.")


# ===========================
# Detail View (Retrieve/Update/Delete) for General Orders
# ===========================
class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    lookup_field = "pk"

    def get_object(self):
        order = super().get_object()
        user = self.request.user

        if user.role == "admin":
            return order
        elif user.role == "manager":
            if not hasattr(user, "restaurant") or order.restaurant != user.restaurant:
                raise PermissionDenied("This order doesn't belong to your restaurant.")
            return order
        elif user.role == "rider":
            rider = get_object_or_404(Rider, user=user)
            if order.rider != rider:
                raise PermissionDenied("You are not assigned to this order.")
            return order
        else:
            raise PermissionDenied("You do not have permission to access this order.")


# ===========================
# List Orders for a Specific Rider
# ===========================
class RiderOrderListView(generics.ListAPIView):
    """
    Admin or Manager can view a specific rider's orders.
    """

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        rider_id = self.kwargs.get("rider_id")

        rider = get_object_or_404(Rider, id=rider_id)

        if user.role == "admin":
            return Order.objects.filter(rider=rider).order_by("-date_ordered")
        elif user.role == "manager":
            if not hasattr(user, "restaurant") or rider.restaurant != user.restaurant:
                raise PermissionDenied("This rider does not belong to your restaurant.")
            return Order.objects.filter(rider=rider).order_by("-date_ordered")

        raise PermissionDenied(
            "You do not have permission to view this rider's orders."
        )


# ===========================
# Create Order for a Rider (Manager Only)
# ===========================
class RiderOrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != "manager":
            raise PermissionDenied("Only managers can create orders.")

        restaurant_id = self.kwargs.get("restaurant_id")
        rider_id = self.kwargs.get("rider_id")

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        rider = get_object_or_404(Rider, id=rider_id)

        if not hasattr(user, "restaurant") or user.restaurant.id != restaurant.id:
            raise PermissionDenied(
                "You can only create orders for your own restaurant."
            )
        if rider.restaurant.id != restaurant.id:
            raise PermissionDenied("This rider does not belong to your restaurant.")

        serializer.save(restaurant=restaurant, rider=rider)


# ===========================
# Retrieve/Update/Delete a Specific Rider's Order
# ===========================
class RiderOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        rider_id = self.kwargs.get("rider_id")

        rider = get_object_or_404(Rider, id=rider_id)

        if user.role == "admin":
            return Order.objects.filter(rider=rider)
        elif user.role == "manager":
            if not hasattr(user, "restaurant") or rider.restaurant != user.restaurant:
                raise PermissionDenied("You do not have access to this rider's orders.")
            return Order.objects.filter(rider=rider)

        raise PermissionDenied("You do not have permission to manage this order.")
