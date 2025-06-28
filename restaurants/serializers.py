from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        exclude = ['user', 'id']  # id is auto-generated, user set in the view

    def create(self, validated_data):
        return Restaurant.objects.create(**validated_data)
