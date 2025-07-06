from rest_framework import serializers
from .models import Restaurant, FoodCategory, Food, Review
from .serializers import (
    FoodCategorySerializer,
    FoodSerializer,
    ReviewSerializer,
)  # Assume these exist


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_image_url = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    foods = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "representative",
            "phone",
            "business_license",
            "owner_nid",
            "established_date",
            "working_period",
            "large_option",
            "location",
            "restaurant_image_url",
            "rating",
            "status",
            "categories",
            "foods",
            "reviews",
        ]

    def get_restaurant_image_url(self, obj):
        request = self.context.get("request")
        if obj.restaurant_image and request:
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None

    def get_categories(self, obj):
        categories = obj.categories.all()
        return (
            FoodCategorySerializer(categories, many=True).data
            if categories.exists()
            else []
        )

    def get_foods(self, obj):
        foods = obj.foods.all()
        return FoodSerializer(foods, many=True).data if foods.exists() else []

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return ReviewSerializer(reviews, many=True).data if reviews.exists() else []
