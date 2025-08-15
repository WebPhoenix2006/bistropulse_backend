from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone

from .models import (
    Restaurant,
    FoodCategory,
    Food,
    Extra,
    Rider,
    ShiftType,
    RiderShift,
)
from .serializers import (
    RestaurantSerializer,
    FoodCategorySerializer,
    FoodSerializer,
    ExtraSerializer,
    RiderSerializer,
    ShiftTypeSerializer,
    RiderShiftSerializer,
)


# 🔒 Force HTTPS in all response URLs
def enforce_https_in_response(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and value.startswith("http://"):
                data[key] = value.replace("http://", "https://", 1)
            elif isinstance(value, (dict, list)):
                enforce_https_in_response(value)
    elif isinstance(data, list):
        for item in data:
            enforce_https_in_response(item)
    return data


# ---------------- RESTAURANTS ----------------
class RestaurantListCreateView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


class RestaurantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


# ---------------- FOOD CATEGORIES ----------------
class FoodCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = FoodCategory.objects.filter(restaurant__user=self.request.user)
        restaurant_id = self.kwargs.get("restaurant_id")
        if restaurant_id:
            qs = qs.filter(restaurant__restaurant_id=restaurant_id)
        return qs

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get("restaurant_id") or self.request.data.get(
            "restaurant"
        )
        restaurant = get_object_or_404(
            Restaurant, restaurant_id=restaurant_id, user=self.request.user
        )
        serializer.save(restaurant=restaurant)

    def get_serializer_context(self):
        return {"request": self.request}


class FoodCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return FoodCategory.objects.filter(restaurant__user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


# ---------------- FOODS ----------------
class FoodListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = Food.objects.filter(restaurant__user=self.request.user)
        restaurant_id = self.kwargs.get("restaurant_id")
        if restaurant_id:
            qs = qs.filter(restaurant__restaurant_id=restaurant_id)
        return qs

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get("restaurant_id") or self.request.data.get(
            "restaurant"
        )
        restaurant = get_object_or_404(
            Restaurant, restaurant_id=restaurant_id, user=self.request.user
        )
        serializer.save(restaurant=restaurant)

    def get_serializer_context(self):
        return {"request": self.request}


class FoodRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "pk"

    def get_queryset(self):
        return Food.objects.filter(restaurant__user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


# ---------------- CATEGORY + FOOD IN ONE GO ----------------
class RestaurantCategoryFoodCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(
            Restaurant, restaurant_id=restaurant_id, user=request.user
        )
        category_name = request.data.get("category_name")
        food_data = request.data.get("food")

        if not category_name or not food_data:
            return Response(
                {"detail": "category_name and food are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        category = FoodCategory.objects.create(
            restaurant=restaurant, name=category_name
        )
        food = Food.objects.create(
            restaurant=restaurant,
            category=category,
            name=food_data.get("name"),
            description=food_data.get("description"),
            price=food_data.get("price"),
        )

        response_data = {
            "category": FoodCategorySerializer(
                category, context={"request": request}
            ).data,
            "food": FoodSerializer(food, context={"request": request}).data,
        }
        return Response(
            enforce_https_in_response(response_data), status=status.HTTP_201_CREATED
        )


# ---------------- EXTRAS ----------------
class ExtraListCreateView(generics.ListCreateAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


# ---------------- RIDERS ----------------
class RiderListCreateView(generics.ListCreateAPIView):
    serializer_class = RiderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = Rider.objects.filter(restaurant__user=self.request.user)
        restaurant_id = self.kwargs.get("restaurant_id")
        if restaurant_id:
            qs = qs.filter(restaurant__restaurant_id=restaurant_id)
        return qs

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get("restaurant_id") or self.request.data.get(
            "restaurant"
        )
        restaurant = get_object_or_404(
            Restaurant, restaurant_id=restaurant_id, user=self.request.user
        )
        serializer.save(restaurant=restaurant)

    def get_serializer_context(self):
        return {"request": self.request}


class RiderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "rider_code"

    def get_queryset(self):
        return Rider.objects.filter(restaurant__user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def toggle_rider_active_status(request, pk):
    rider = get_object_or_404(Rider, pk=pk, restaurant__user=request.user)
    rider.is_active = not rider.is_active
    rider.save()
    return Response(
        {
            "id": rider.id,
            "full_name": rider.full_name,
            "is_active": rider.is_active,
            "message": f"Rider is now {'active' if rider.is_active else 'inactive'}",
        },
        status=status.HTTP_200_OK,
    )


# ---------------- SHIFTS ----------------
class ShiftTypeListCreateView(generics.ListCreateAPIView):
    queryset = ShiftType.objects.all()
    serializer_class = ShiftTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


class RiderShiftListView(generics.ListAPIView):
    serializer_class = RiderShiftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RiderShift.objects.filter(rider__restaurant__user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


class StartRiderShiftView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, rider_id):
        shift_type_id = request.data.get("shift_type_id")
        rider = get_object_or_404(Rider, id=rider_id, restaurant__user=request.user)
        shift_type = get_object_or_404(ShiftType, id=shift_type_id)
        shift = RiderShift.objects.create(
            rider=rider, shift_type=shift_type, started_by=request.user
        )
        serializer = RiderShiftSerializer(shift, context={"request": request})
        return Response(enforce_https_in_response(serializer.data), status=201)


class EndRiderShiftView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        secret_code = request.data.get("secret_code")
        shift = get_object_or_404(
            RiderShift, id=pk, rider__restaurant__user=request.user
        )

        if shift.status != "started":
            return Response({"detail": "Shift already ended or cancelled."}, status=400)

        shift.status = "ended"
        shift.secret_code = secret_code
        shift.ended_by = request.user
        shift.end_time = timezone.now()
        shift.save()

        serializer = RiderShiftSerializer(shift, context={"request": request})
        return Response(enforce_https_in_response(serializer.data), status=200)
