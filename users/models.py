from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    otp = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class RoleOTP(models.Model):
    otp = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.otp} → {self.role}"

