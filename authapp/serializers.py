from rest_framework import serializers
from users.models import RoleOTP, User  # make sure this User is your custom user model

class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "fullname", "phone", "otp"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        otp_code = validated_data.pop("otp")
        fullname = validated_data.pop("fullname", "")
        phone = validated_data.pop("phone", "")

        # ✅ Fix: Use the correct field name "otp", not "code"
        try:
            otp = RoleOTP.objects.get(otp=otp_code, is_used=False)
        except RoleOTP.DoesNotExist:
            raise serializers.ValidationError({"otp": "Invalid or expired OTP"})

        # Optional: split fullname into first/last names
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
            phone=phone,  # ✅ make sure your custom User model has this
            role=otp.role  # ✅ make sure your User model has this too
        )

        otp.is_used = True
        otp.save()

        return user
