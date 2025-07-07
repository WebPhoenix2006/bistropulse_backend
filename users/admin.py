from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .models import RoleOTP


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('role', 'otp')}),
    )

admin.site.register(User, UserAdmin)


admin.site.register(RoleOTP)