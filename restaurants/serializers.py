from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',  
            'name',
            'representative',
            'phone',
            'business_license',
            'owner_nid',
            'established_date',
            'working_period',
            'large_option',
            'location',
            'restaurant_image',
            'rating',
            'status',
        ]
