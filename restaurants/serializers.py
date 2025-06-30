from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'representative', 'phone', 'business_license',
            'owner_nid', 'established_date', 'working_period', 'large_option',
            'location', 'restaurant_image_url', 'rating', 'status'
        ]
        read_only_fields = ['restaurant_image_url']

    def get_restaurant_image_url(self, obj):
        request = self.context.get('request')
        if obj.restaurant_image and request:
            return request.build_absolute_uri(obj.restaurant_image.url)
        return None

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user', None)
        return Restaurant.objects.create(user=user, **validated_data)
