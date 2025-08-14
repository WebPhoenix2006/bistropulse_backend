from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .serializers import OrderSerializer
from .models import Order
from restaurants.models import Restaurant, Rider


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Order.objects.all().order_by("-date_ordered")
        elif user.role == "manager":
            if not hasattr(user, "restaurant"):
                raise PermissionDenied("Manager is not associated with any restaurant.")
            return Order.objects.filter(
                restaurant__restaurant_id=user.restaurant.restaurant_id
            ).order_by("-date_ordered")
        elif user.role == "rider":
            rider = get_object_or_404(Rider, user=user)
            return Order.objects.filter(rider__rider_code=rider.rider_code).order_by(
                "-date_ordered"
            )
        return Order.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if hasattr(self.request.user, "restaurant"):
            context["restaurant_id"] = self.request.user.restaurant.restaurant_id
        return context

    def perform_create(self, serializer):
        user = self.request.user
        if user.role not in ["manager", "admin"]:
            raise PermissionDenied("Only managers or admins can create orders.")
        serializer.save()


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    lookup_field = "order_id"

    def get_object(self):
        order = super().get_object()
        user = self.request.user

        if user.role == "admin":
            return order
        elif user.role == "manager":
            if (
                not hasattr(user, "restaurant")
                or order.restaurant.restaurant_id != user.restaurant.restaurant_id
            ):
                raise PermissionDenied("This order doesn't belong to your restaurant.")
            return order
        elif user.role == "rider":
            rider = get_object_or_404(Rider, user=user)
            if order.rider.rider_code != rider.rider_code:
                raise PermissionDenied("You are not assigned to this order.")
            return order
        else:
            raise PermissionDenied("You do not have permission to access this order.")


class RestaurantOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "order_id"

    def get_queryset(self):
        restaurant_id = self.kwargs.get("restaurant_id")
        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        user = self.request.user

        if user.role == "admin":
            return Order.objects.filter(
                restaurant__restaurant_id=restaurant.restaurant_id
            )
        elif user.role == "manager":
            if (
                not hasattr(user, "restaurant")
                or user.restaurant.restaurant_id != restaurant.restaurant_id
            ):
                raise PermissionDenied(
                    "You can only manage orders for your own restaurant."
                )
            return Order.objects.filter(
                restaurant__restaurant_id=restaurant.restaurant_id
            )
        else:
            raise PermissionDenied("You do not have permission to manage this order.")


class RiderOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        rider_code = self.kwargs.get("rider_code")
        rider = get_object_or_404(Rider, rider_code=rider_code)

        if user.role == "admin":
            return Order.objects.filter(rider__rider_code=rider.rider_code).order_by(
                "-date_ordered"
            )
        elif user.role == "manager":
            if (
                not hasattr(user, "restaurant")
                or rider.restaurant.restaurant_id != user.restaurant.restaurant_id
            ):
                raise PermissionDenied("This rider does not belong to your restaurant.")
            return Order.objects.filter(rider__rider_code=rider.rider_code).order_by(
                "-date_ordered"
            )

        raise PermissionDenied(
            "You do not have permission to view this rider's orders."
        )


class RiderOrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "manager":
            raise PermissionDenied("Only managers can create orders.")

        restaurant_id = self.kwargs.get("restaurant_id")
        rider_code = self.kwargs.get("rider_code")

        restaurant = get_object_or_404(Restaurant, restaurant_id=restaurant_id)
        rider = get_object_or_404(Rider, rider_code=rider_code)

        if (
            not hasattr(user, "restaurant")
            or user.restaurant.restaurant_id != restaurant.restaurant_id
        ):
            raise PermissionDenied(
                "You can only create orders for your own restaurant."
            )
        if rider.restaurant.restaurant_id != restaurant.restaurant_id:
            raise PermissionDenied("This rider does not belong to your restaurant.")

        serializer.save(restaurant=restaurant, rider=rider)


class RiderOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "order_id"

    def get_queryset(self):
        user = self.request.user
        rider_code = self.kwargs.get("rider_code")
        rider = get_object_or_404(Rider, rider_code=rider_code)

        if user.role == "admin":
            return Order.objects.filter(rider__rider_code=rider.rider_code)
        elif user.role == "manager":
            if (
                not hasattr(user, "restaurant")
                or rider.restaurant.restaurant_id != user.restaurant.restaurant_id
            ):
                raise PermissionDenied("You do not have access to this rider's orders.")
            return Order.objects.filter(rider__rider_code=rider.rider_code)

        raise PermissionDenied("You do not have permission to manage this order.")
