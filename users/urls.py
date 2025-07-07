from django.urls import path
from .views import RegisterView, RoleOTPListCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('role-otps/', RoleOTPListCreateView.as_view(), name='role-otp-list-create'),
]
