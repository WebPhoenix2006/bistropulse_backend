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

# ─────────────────────────────
# 📦 RESTAURANT CRUD
# ─────────────────────────────


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


# ─────────────────────────────
# 🍽️ FOOD CATEGORY CRUD
# ─────────────────────────────


class FoodCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FoodCategory.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get("restaurant_id")
        serializer.save(restaurant_id=restaurant_id)

    def get_serializer_context(self):
        return {"request": self.request}


# ─────────────────────────────
# 🍔 FOOD CRUD
# ─────────────────────────────


class FoodListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Food.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get("restaurant")
        serializer.save(restaurant_id=restaurant_id)

    def get_serializer_context(self):
        return {"request": self.request}


class RestaurantFoodListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        restaurant_id = self.kwargs["restaurant_id"]
        return Food.objects.filter(
            restaurant__id=restaurant_id, restaurant__user=self.request.user
        )

    def perform_create(self, serializer):
        restaurant_id = self.kwargs["restaurant_id"]
        serializer.save(restaurant_id=restaurant_id)

    def get_serializer_context(self):
        return {"request": self.request}


# ─────────────────────────────
# ➕ EXTRAS CRUD
# ─────────────────────────────


class ExtraListCreateView(generics.ListCreateAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


# ─────────────────────────────
# 🚴‍♂️ RIDER CRUD
# ─────────────────────────────


class RiderListCreateView(generics.ListCreateAPIView):
    serializer_class = RiderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Rider.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_context(self):
        return {"request": self.request}


class RiderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Rider.objects.filter(restaurant__user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


# 🔄 TOGGLE RIDER ACTIVE STATUS
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def toggle_rider_active_status(request, pk):
    try:
        rider = Rider.objects.get(pk=pk, restaurant__user=request.user)
    except Rider.DoesNotExist:
        return Response(
            {"detail": "Rider not found."}, status=status.HTTP_404_NOT_FOUND
        )

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


# ─────────────────────────────
# 🕓 SHIFT TYPES
# ─────────────────────────────


class ShiftTypeListCreateView(generics.ListCreateAPIView):
    queryset = ShiftType.objects.all()
    serializer_class = ShiftTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


# ─────────────────────────────
# 🕒 RIDER SHIFTS
# ─────────────────────────────


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

        try:
            rider = Rider.objects.get(id=rider_id, restaurant__user=request.user)
            shift_type = ShiftType.objects.get(id=shift_type_id)
        except (Rider.DoesNotExist, ShiftType.DoesNotExist):
            return Response({"detail": "Rider or shift type not found."}, status=404)

        shift = RiderShift.objects.create(
            rider=rider, shift_type=shift_type, started_by=request.user
        )
        serializer = RiderShiftSerializer(shift, context={"request": request})
        return Response(serializer.data, status=201)


class EndRiderShiftView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        secret_code = request.data.get("secret_code")

        try:
            shift = RiderShift.objects.get(id=pk, rider__restaurant__user=request.user)
        except RiderShift.DoesNotExist:
            return Response({"detail": "Shift not found."}, status=404)

        if shift.status != "started":
            return Response({"detail": "Shift already ended or cancelled."}, status=400)

        shift.status = "ended"
        shift.secret_code = secret_code
        shift.ended_by = request.user
        shift.end_time = timezone.now()
        shift.save()

        serializer = RiderShiftSerializer(shift, context={"request": request})
        return Response(serializer.data, status=200)


class RestaurantRiderListView(generics.ListAPIView):
    serializer_class = RiderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs.get("restaurant_id")
        return Rider.objects.filter(
            restaurant__id=restaurant_id, restaurant__user=self.request.user
        )

    def get_serializer_context(self):
        return {"request": self.request}
