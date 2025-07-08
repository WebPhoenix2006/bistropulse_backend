from rest_framework import serializers
from .models import User, RoleOTP


class SignupSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "otp_code", "phone", "fullname"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_otp_code(self, value):
        try:
            role_otp = RoleOTP.objects.get(otp=value, is_used=False)
            self.role = role_otp
            return value
        except RoleOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired OTP code.")

    def create(self, validated_data):
        validated_data.pop("otp_code")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            phone=validated_data.get("phone"),
            fullname=validated_data.get("fullname"),
            role=self.role.role,  # access role from RoleOTP
        )

        self.role.is_used = True
        self.role.save()

        return user


# ✅ Add this to fix the ImportError
class RoleOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleOTP
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']