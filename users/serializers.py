from rest_framework import serializers
from users.models import User, RoleOTP

class RegisterSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'otp']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        otp_code = validated_data.pop('otp')

        try:
            otp = RoleOTP.objects.get(code=otp_code, is_used=False)
        except RoleOTP.DoesNotExist:
            raise serializers.ValidationError({'otp': 'Invalid or expired OTP'})

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=otp.role
        )

        otp.is_used = True
        otp.save()

        return user
