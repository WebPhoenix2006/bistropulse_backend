from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import User, RoleOTP  # 👈 Import your models


class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "fullname", "phone"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        fullname = validated_data.pop("fullname", "")
        phone = validated_data.pop(
            "phone", ""
        )  # you can just accept it, even if unused

        # Split fullname
        first_name = ""
        last_name = ""
        if " " in fullname:
            first_name, last_name = fullname.split(" ", 1)
        else:
            first_name = fullname

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=first_name,
            last_name=last_name,
        )

        # No profile model, so we ignore phone (or you can print/save elsewhere)

        return user


class RegisterSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "otp"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        otp_code = validated_data.pop("otp")
        try:
            otp = RoleOTP.objects.get(code=otp_code, is_used=False)
        except RoleOTP.DoesNotExist:
            raise serializers.ValidationError({"otp": "Invalid or expired OTP"})

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            role=otp.role,
        )
        otp.is_used = True
        otp.save()
        return user
