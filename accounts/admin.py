from django.contrib import admin
from .models import User, OTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_admin', 'is_superuser', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_admin', 'is_superuser')
    ordering = ('email',)

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'created_at', 'expires_at')
    search_fields = ('user__email', 'otp_code')
    list_filter = ('created_at', 'expires_at')
