from rest_framework import serializers
from .models import Restaurant, Representative, FoodCategory, Extra, Food, Review


# ✅ Updated: Added photo_url field to return full image URL of representative


class RepresentativeSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()  # ✅ Computed image URL

    class Meta:
        model = Representative
        fields = ["id", "full_name", "photo", "photo_url", "phone", "location"]

    def get_photo_url(self, obj):
        request = self.context.get("request")
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None



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
    restaurant_image = serializers.ImageField(required=False)
    representative = RepresentativeSerializer()  # ✅ Nested representative object
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
            "restaurant_image",
            "restaurant_image_url",
            "rating",
            "status",
            "categories",
            "foods",
            "reviews",
        ]

    def get_restaurant_image_url(self, obj):
        # ✅ Build full image URL for restaurant image
        request = self.context.get("request")
        if obj.restaurant_image and request:
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None

    def create(self, validated_data):
        # ✅ Handle nested representative object creation
        rep_data = validated_data.pop("representative", None)
        if rep_data:
            rep = Representative.objects.create(**rep_data)
            validated_data["representative"] = rep
        return Restaurant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # ✅ Handle nested representative object update or creation
        rep_data = validated_data.pop("representative", None)
        if rep_data:
            if instance.representative:
                for attr, value in rep_data.items():
                    setattr(instance.representative, attr, value)
                instance.representative.save()
            else:
                rep = Representative.objects.create(**rep_data)
                instance.representative = rep
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
