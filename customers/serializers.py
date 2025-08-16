import os
from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'customer_id', 'name', 'email', 'phone',
            'is_student', 'gender', 'location', 'photo', 'photo_url', 'created_at'
        ]
        read_only_fields = ['customer_id', 'created_at', 'photo_url']
        extra_kwargs = {
            'photo': {'write_only': True}  # Prevents photo from appearing in responses
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        
        # Remove user if accidentally included
        validated_data.pop('user', None)
        
        # Create the customer instance
        customer = Customer.objects.create(user=user, **validated_data)
        
       
        
        return customer

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.photo.url)
            # Fallback if no request in context (shouldn't happen in normal API usage)
            return obj.photo.url
        return None