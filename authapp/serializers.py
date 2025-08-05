from rest_framework import serializers
from users.models import RoleOTP, User  # make sure this User is your custom user model

class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)  # 🔥 role is sent explicitly

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "fullname", "phone", "role", "otp"]
        extra_kwargs = {
            "password": {"write_only": True},
            "otp": {"write_only": True, "required": False},  # 💥 optional at all times
        }

    def validate(self, attrs):
        role = attrs.get("role")
        otp_code = attrs.get("otp")

        if role != "admin":
            if not otp_code:
                raise serializers.ValidationError({"otp": "OTP is required for this role."})
            if not RoleOTP.objects.filter(otp=otp_code, is_used=False, role=role).exists():
                raise serializers.ValidationError({"otp": "Invalid or expired OTP."})
        
        return attrs

    def create(self, validated_data):
        otp_code = validated_data.pop("otp", None)
        fullname = validated_data.pop("fullname", "")
        phone = validated_data.pop("phone", "")
        role = validated_data.pop("role", "admin")

        first_name, last_name = "", ""
        if " " in fullname:
            first_name, last_name = fullname.split(" ", 1)
        else:
            first_name = fullname

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
        )

        if role != "admin" and otp_code:
            otp = RoleOTP.objects.get(otp=otp_code, is_used=False, role=role)
            otp.is_used = True
            otp.save()

        return user
