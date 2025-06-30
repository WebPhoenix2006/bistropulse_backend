from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'customer_id', 'name', 'email', 'phone',
            'is_student', 'gender', 'location', 'photo', 'created_at'
        ]
        read_only_fields = ['customer_id', 'created_at', 'photo']

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None

    def create(self, validated_data):
        user = self.context['request'].user  # get user from request
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
