from datetime import date
from rest_framework import serializers
from .models import (
    Restaurant,
    Representative,
    FoodCategory,
    Extra,
    Food,
    Review,
    Rider,
    RiderShift,
    ShiftType,
)


class RepresentativeSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    photo_url = serializers.SerializerMethodField()

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


class RiderSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Rider
        fields = [
            "id",
            "rider_code",
            "full_name",
            "phone",
            "profile_image",
            "profile_image_url",
            "date_of_birth",
            "gender",
            "address",
            "restaurant",
            "is_active",
        ]
        read_only_fields = ["rider_code"]

    def get_profile_image_url(self, obj):
        request = self.context.get("request")
        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return None

    def validate_date_of_birth(self, value):
        if value:
            today = date.today()
            age = (
                today.year
                - value.year
                - ((today.month, today.day) < (value.month, value.day))
            )
            if age < 18:
                raise serializers.ValidationError(
                    "Rider must be at least 18 years old."
                )
        return value


class ShiftTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftType
        fields = ["id", "name", "start_time", "end_time"]


class RiderShiftSerializer(serializers.ModelSerializer):
    rider_name = serializers.CharField(source="rider.full_name", read_only=True)
    shift_type_name = serializers.CharField(source="shift_type.name", read_only=True)

    class Meta:
        model = RiderShift
        fields = [
            "id",
            "rider",
            "rider_name",
            "shift_type",
            "shift_type_name",
            "start_time",
            "end_time",
            "status",
            "secret_code",
            "started_by",
            "ended_by",
        ]
        read_only_fields = [
            "start_time",
            "status",
            "started_by",
            "ended_by",
            "end_time",
        ]


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_image_url = serializers.SerializerMethodField()
    restaurant_image = serializers.ImageField(required=False)
    representative = RepresentativeSerializer()
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
        request = self.context.get("request")
        if obj.restaurant_image and request:
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None

    def create(self, validated_data):
        rep_data = validated_data.pop("representative", {})
        request = self.context.get("request")

        # Support nested file fields
        if request and hasattr(request, "FILES"):
            if "representative.photo" in request.FILES:
                rep_data["photo"] = request.FILES["representative.photo"]
            if "restaurant_image" in request.FILES:
                validated_data["restaurant_image"] = request.FILES["restaurant_image"]

        rep = Representative.objects.create(**rep_data)
        validated_data["representative"] = rep
        return Restaurant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        rep_data = validated_data.pop("representative", {})
        request = self.context.get("request")

        if request and hasattr(request, "FILES"):
            if "representative.photo" in request.FILES:
                rep_data["photo"] = request.FILES["representative.photo"]
            if "restaurant_image" in request.FILES:
                validated_data["restaurant_image"] = request.FILES["restaurant_image"]

        # Update or create nested representative
        if rep_data:
            if instance.representative:
                for attr, value in rep_data.items():
                    setattr(instance.representative, attr, value)
                instance.representative.save()
            else:
                instance.representative = Representative.objects.create(**rep_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
