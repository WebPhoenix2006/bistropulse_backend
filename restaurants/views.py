from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Restaurant, FoodCategory, Food, Extra
from .serializers import (
    RestaurantSerializer,
    FoodCategorySerializer,
    FoodSerializer,
    ExtraSerializer,
)


class RestaurantListCreateView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print("🔍 Incoming FILES:", self.request.FILES)
        print("📥 restaurant_image:", self.request.FILES.get("restaurant_image"))
        print("📤 DATA:", self.request.data)
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


class ExtraListCreateView(generics.ListCreateAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}
