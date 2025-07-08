from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response(
                {
                    "token": token.key,
                    "user": {
                        "id": user.id,  # ✅ add this
                        "username": user.username,
                        "role": user.role,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        print("Register failed:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key,
                    "user": {
                        "id": user.id,  # ✅ add this
                        "username": user.username,
                        "role": user.role,
                    },
                }
            )

        print("Login failed for:", request.data)
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

