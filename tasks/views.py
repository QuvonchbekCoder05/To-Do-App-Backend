from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Task, SpecialTask
from .serializers import TaskSerializer, SpecialTaskSerializer

# Oddiy Task API
class TaskAPIView(APIView):
    # JWT autentifikatsiyasi va IsAuthenticated ruxsatini qo'shamiz
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Foydalanuvchining Tasklarini olish uchun GET so'rovi.
        Filtr parametri `daily`, `weekly`, `monthly` orqali berib olamiz .
        """
        filter_param = request.query_params.get('filter')
        tasks = Task.objects.filter(user=request.user)

        # Filtr shartlarini aniqlash
        today = timezone.now().date()
        current_week = today.isocalendar()[1]
        current_month = today.month

        # Parametrga qarab filtrni qo'llab chiqamiz
        if filter_param == 'daily':
            tasks = tasks.filter(due_date=today)
        elif filter_param == 'weekly':
            tasks = tasks.filter(due_date__week=current_week)
        elif filter_param == 'monthly':
            tasks = tasks.filter(due_date__month=current_month)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Yangi task yaratish uchun POST so'rovi.
        """
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Taskni yangilash uchun PUT so'rovi.
        """
        task = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Taskni o'chirish uchun DELETE so'rovi.
        """
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Maxsus Task (SpecialTask) API
class SpecialTaskAPIView(APIView):
    # JWT autentifikatsiyasi va IsAuthenticated ruxsatini qo'shamiz
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Maxsus sanaga asoslangan SpecialTasklarni olish uchun GET so'rovi.
        """
        special_date = request.query_params.get('special_date')
        tasks = SpecialTask.objects.filter(user=request.user)

        if special_date:
            tasks = tasks.filter(special_date=special_date)

        serializer = SpecialTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Yangi SpecialTask yaratish uchun POST so'rovi.
        """
        serializer = SpecialTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        SpecialTaskni yangilash uchun PUT so'rovi.
        """
        task = get_object_or_404(SpecialTask, pk=pk, user=request.user)
        serializer = SpecialTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        SpecialTaskni o'chirish uchun DELETE so'rovi.
        """
        task = get_object_or_404(SpecialTask, pk=pk, user=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
