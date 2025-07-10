from rest_framework import serializers
from .models import Restaurant, FoodCategory, Extra, Food, Review


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ["id", "name"]


class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = ["id", "name", "price"]


class FoodSerializer(serializers.ModelSerializer):
    extras = ExtraSerializer(many=True, read_only=True)

    class Meta:
        model = Food
        fields = ["id", "name", "description", "price", "category", "image", "extras"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "comment", "rating", "created_at"]


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_image_url = serializers.SerializerMethodField()
    restaurant_image = serializers.ImageField(required=False)  # ✅ Add this
    categories = FoodCategorySerializer(many=True, read_only=True)
    foods = FoodSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

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
            "restaurant_image",  # ✅ Add this line
            "restaurant_image_url",  # This one stays for the frontend
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
