from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .models import Restaurant, Food, Extra, FoodCategory
from .serializers import (
    RestaurantSerializer,
    FoodSerializer,
    ExtraSerializer,
    FoodCategorySerializer,
)


class RestaurantListCreateView(ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Accept FormData

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FoodCategoryListCreateView(ListCreateAPIView):
    serializer_class = FoodCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodCategory.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get("restaurant_id")
        if not restaurant_id:
            raise serializers.ValidationError("restaurant_id is required")
        serializer.save(restaurant_id=restaurant_id)


class ExtraListCreateView(ListCreateAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
    permission_classes = [IsAuthenticated]


class FoodListCreateView(ListCreateAPIView):
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Food.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get("restaurant")
        category_id = self.request.data.get("category")

        if not restaurant_id:
            raise serializers.ValidationError("restaurant is required")

        serializer.save(restaurant_id=restaurant_id, category_id=category_id)
