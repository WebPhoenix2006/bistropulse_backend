from rest_framework import serializers
from .models import User, RoleOTP

class SignupSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(write_only=True)  # input only

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'otp_code', 'phone', 'fullname']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_otp_code(self, value):
        try:
            role_otp = RoleOTP.objects.get(otp=value)
            self.role = role_otp.role  # stash it
            return value
        except RoleOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired OTP code.")

    def create(self, validated_data):
        validated_data.pop('otp_code')  # remove from data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            role=self.role
        )
        return user

class RoleOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleOTP
        fields = '__all__'
