from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from users.models import RoleOTP
from users.serializers import RoleOTPSerializer, SignupSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response(
                {
                    "token": token.key,
                    "user": {
                        "username": user.username,
                        "role": user.role,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleOTPListCreateView(generics.ListCreateAPIView):
    queryset = RoleOTP.objects.all().order_by("-created_at")
    serializer_class = RoleOTPSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # You can replace with IsSuperAdmin later
