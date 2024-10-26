from django.contrib import admin
from .models import SpecialTask

@admin.register(SpecialTask)
class SpecialTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'special_date', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__email')
    list_filter = ('status', 'special_date', 'created_at', 'updated_at')
    ordering = ('special_date', 'status')
