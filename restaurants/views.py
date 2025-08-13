# views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, serializers
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
    
 
class RestaurantCategoryFoodCreateView(APIView):
    """
    Create a FoodCategory and Food in a single request for a given restaurant.
    Expected payload:
    {
        "category_name": "Burgers",
        "food": {
            "name": "Cheese Burger",
            "description": "Juicy beef patty with cheese",
            "price": 2500
        }
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, restaurant_id):
        # Make sure the restaurant belongs to the logged-in user
        restaurant = get_object_or_404(Restaurant, id=restaurant_id, user=request.user)

        category_name = request.data.get("category_name")
        food_data = request.data.get("food")

        if not category_name or not food_data:
            return Response(
                {"detail": "category_name and food are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create category
        category = FoodCategory.objects.create(
            restaurant=restaurant,
            name=category_name
        )

        # Create food
        food = Food.objects.create(
            restaurant=restaurant,
            category=category,
            name=food_data.get("name"),
            description=food_data.get("description"),
            price=food_data.get("price"),
        )

        return Response({
            "category": FoodCategorySerializer(category, context={"request": request}).data,
            "food": FoodSerializer(food, context={"request": request}).data
        }, status=status.HTTP_201_CREATED)
    


class ExtraListCreateView(generics.ListCreateAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


class RiderListCreateView(generics.ListCreateAPIView):
    serializer_class = RiderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        restaurant_id = self.kwargs.get("restaurant_id")
        if restaurant_id:
            return Rider.objects.filter(
                restaurant__id=restaurant_id, restaurant__user=self.request.user
            )
        return Rider.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get("restaurant_id")
        if restaurant_id:
            restaurant = Restaurant.objects.filter(
                id=restaurant_id, user=self.request.user
            ).first()
            if not restaurant:
                raise serializers.ValidationError(
                    {
                        "restaurant": f'Invalid restaurant ID "{restaurant_id}" - object does not exist.'
                    }
                )
            serializer.validated_data.pop("restaurant", None)
            serializer.save(restaurant=restaurant)
        else:
            serializer.save()  # Restaurant must be passed via form if not in URL

    def get_serializer_context(self):
        return {"request": self.request}


class RiderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'rider_code'  # 👈🔥 This line allows you to look up each rider by their code instead of default django id: 1,2,3


    def get_queryset(self):
        return Rider.objects.filter(restaurant__user=self.request.user)

    def get_serializer_context(self):
        return {"request": self.request}


class RestaurantRiderListView(generics.ListCreateAPIView):
    serializer_class = RiderSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        restaurant_id = self.kwargs.get("restaurant_id")
        return Rider.objects.filter(
            restaurant__id=restaurant_id, restaurant__user=self.request.user
        )

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get("restaurant_id")
        restaurant = Restaurant.objects.filter(
            id=restaurant_id, user=self.request.user
        ).first()
        if not restaurant:
            raise serializers.ValidationError(
                {
                    "restaurant": f'Invalid restaurant ID "{restaurant_id}" - object does not exist.'
                }
            )

        # Prevent required field error
        serializer.validated_data.pop("restaurant", None)
        serializer.save(restaurant=restaurant)

    def get_serializer_context(self):
        return {"request": self.request}


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


