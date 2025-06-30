from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'customer_id', 'name', 'email', 'phone',
            'is_student', 'gender', 'location', 'photo', 'created_at'
        ]

    def get_photo(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.photo.url) if obj.photo and request else None

