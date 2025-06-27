from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'fullname', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        fullname = validated_data.pop('fullname', '')
        phone = validated_data.pop('phone', '')  # you can just accept it, even if unused

        # Split fullname
        first_name = ''
        last_name = ''
        if ' ' in fullname:
            first_name, last_name = fullname.split(' ', 1)
        else:
            first_name = fullname

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )

        # No profile model, so we ignore phone (or you can print/save elsewhere)

        return user
