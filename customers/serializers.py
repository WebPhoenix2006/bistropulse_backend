from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'customer_id', 'name', 'email', 'phone',
            'is_student', 'gender', 'location', 'photo_url', 'created_at'
        ]
        read_only_fields = ['customer_id', 'created_at', 'photo_url']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if not obj.photo:
            print("No photo saved for this object")
        if not hasattr(obj.photo, 'url'):
            print("Photo object has no URL")
        if not request:
            print("No request in serializer context")
        if obj.photo and hasattr(obj.photo, 'url') and request:
            return request.build_absolute_uri(obj.photo.url)
        return None



    def create(self, validated_data):
        print("Incoming FILES:", self.context['request'].FILES)  # <- check if 'photo' is present
        user = self.context['request'].user
        validated_data.pop('user', None)
        return Customer.objects.create(user=user, **validated_data)
