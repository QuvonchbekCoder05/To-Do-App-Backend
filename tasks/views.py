from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Task, SpecialTask
from .serializers import TaskSerializer, SpecialTaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        filter_param = self.request.query_params.get('filter')

        if filter_param == 'daily':
            due_date_filter = timezone.now().date()
        elif filter_param == 'weekly':
            due_date_filter = timezone.now().isocalendar()[1]
        elif filter_param == 'monthly':
            due_date_filter = timezone.now().month
        else:
            due_date_filter = None

        if due_date_filter:
            return Task.objects.filter(user=user, due_date=due_date_filter)
        else:
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