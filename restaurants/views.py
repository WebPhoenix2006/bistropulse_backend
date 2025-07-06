from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Restaurant, Food, Extra, FoodCategory
from .serializers import (
    RestaurantSerializer,
    FoodSerializer,
    ExtraSerializer,
    FoodCategorySerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, permissions


class RestaurantListCreateView(ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Accept FormData

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FoodCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FoodCategory.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get("restaurant_id")
        serializer.save(restaurant_id=restaurant_id)


class ExtraListCreateView(generics.ListCreateAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
    permission_classes = [permissions.IsAuthenticated]


class FoodListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Food.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get("restaurant")
        serializer.save(restaurant_id=restaurant_id)
