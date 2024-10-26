# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Task, SpecialTask
from .serializers import TaskSerializer, SpecialTaskSerializer

class TaskViewSet(viewsets.ModelViewSet): #Foydalanuvchilar uchun vazifalar ustida ishlash imkoniyatini beruvchi viewset yaratib olgan qismim
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        filter_param = self.request.query_params.get('filter')# URL dan filtr parametrini olamiz 
        user = self.request.user  # Hozirgi foydalanuvchini olamiz 
        if filter_param == 'daily': # Agar "daily" filtri bo'lsa
            return Task.objects.filter(user=user, due_date=timezone.now().date()) # Bugungi vazifalar qaytaramiz qolganlari ham shu ketma ketlikda boladi
        elif filter_param == 'weekly':
            return Task.objects.filter(user=user, due_date__week=timezone.now().isocalendar()[1])
        elif filter_param == 'monthly':
            return Task.objects.filter(user=user, due_date__month=timezone.now().month)
        return Task.objects.filter(user=user)


class SpecialTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SpecialTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        special_date = self.request.query_params.get('special_date')
        if special_date:
            return SpecialTask.objects.filter_by_special_day(user=user, date=special_date)
        return SpecialTask.objects.filter(user=user)
