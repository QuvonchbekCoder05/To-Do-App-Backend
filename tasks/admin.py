from django.contrib import admin
from .models import Task, SpecialTask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'due_date', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__email')
    list_filter = ('status', 'due_date', 'created_at', 'updated_at')
    ordering = ('due_date', 'status')
    date_hierarchy = 'due_date'

@admin.register(SpecialTask)
class SpecialTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'special_date', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__email')
    list_filter = ('status', 'special_date', 'created_at', 'updated_at')
    ordering = ('special_date', 'status')
    date_hierarchy = 'special_date'
