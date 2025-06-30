from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['user']
        
    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None
