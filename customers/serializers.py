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
        try:
            if obj.photo and obj.photo.name and request:
                return request.build_absolute_uri(obj.photo.url)
        except ValueError:
            # Photo field is set but file is missing — avoid crashing
            return None
        return None




    def create(self, validated_data):
        print("Incoming FILES:", self.context['request'].FILES)  # <- check if 'photo' is present
        user = self.context['request'].user
        validated_data.pop('user', None)
        return Customer.objects.create(user=user, **validated_data)
