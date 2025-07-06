from rest_framework import serializers
from .models import Restaurant, Food, Extra, FoodCategory


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_image_url = serializers.SerializerMethodField(read_only=True)

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
        ]
        read_only_fields = ["restaurant_image_url"]

    def get_restaurant_image_url(self, obj):
        request = self.context.get("request")
        if obj.restaurant_image and request:
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.pop("user", None)
        return Restaurant.objects.create(user=user, **validated_data)


class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = ["id", "name", "price"]


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ["id", "name"]


class FoodSerializer(serializers.ModelSerializer):
    extras = ExtraSerializer(many=True, read_only=True)
    category = FoodCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=FoodCategory.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Food
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "category",
            "category_id",
            "extras",
            "restaurant",
        ]


def get_categories(self, obj):
    return (
        FoodCategorySerializer(obj.categories.all(), many=True).data
        if obj.categories.exists()
        else []
    )


def get_foods(self, obj):
    return (
        FoodCategory(obj.categories.all(), many=True).data
        if obj.categories.exists()
        else []
    )


def get_extras(self, obj):
    return (
        Extra(obj.categories.all(), many=True).data if obj.categories.exists() else []
    )
