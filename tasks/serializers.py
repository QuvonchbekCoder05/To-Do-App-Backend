from rest_framework import serializers
from .models import Task, SpecialTask

class BaseTaskSerializer(serializers.ModelSerializer):
    """Umumiy task maydonlarini saqlash uchun asosiy serializer."""
    class Meta:
        fields = ['id', 'user', 'title', 'description', 'status', 'created_at', 'updated_at']
        

class TaskSerializer(BaseTaskSerializer):
    """Oddiy Task uchun serializer."""
    class Meta(BaseTaskSerializer.Meta):
        model = Task
        fields = BaseTaskSerializer.Meta.fields + ['due_date']

class SpecialTaskSerializer(BaseTaskSerializer):
    """Special Task uchun serializer."""
    class Meta(BaseTaskSerializer.Meta):
        model = SpecialTask
        fields = BaseTaskSerializer.Meta.fields + ['special_date']
