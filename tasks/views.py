from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Task, SpecialTask
from .serializers import TaskSerializer, SpecialTaskSerializer

# Task API
class TaskAPIView(APIView):
    # JWT autentifikatsiyasi va IsAuthenticated talabini qoshamiz 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Tasklar ro‘yxatini olish uchun GET so‘rovini yuboramiz .
        """
        filter_param = request.query_params.get('filter') # So'rov parametrlari orasidan 'filter' ni ajaratib olamiz 
        tasks = Task.objects.filter(user=request.user)  # Foydalanuvchiga tegishli tasklarni olamiz
        
        if filter_param == 'daily':
            tasks = tasks.filter(due_date=timezone.now().date())
        elif filter_param == 'weekly':
            tasks = tasks.filter(due_date__week=timezone.now().isocalendar()[1])
        elif filter_param == 'monthly':
            tasks = tasks.filter(due_date__month=timezone.now().month)

        serializer = TaskSerializer(tasks, many=True)#many true qoyilganing sababi 1 nechat obyektlarni serializatsiya qilmpoqdaiz 
        return Response(serializer.data)

    def post(self, request):
        """
        Yangi task yaratish uchun POST so'rovi yuboramiz .
        """
        serializer = TaskSerializer(data=request.data) # So'rovdan kelgan ma'lumotlar bilan serializerni yaratib olamiz 
        if serializer.is_valid():# Agar ma'lumotlar to'g'ri bo'lsa
            serializer.save(user=request.user) # Oddiu taskni saqlaymiz va foydalanuvchini ulaymiz
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Taskni yangilash uchun PUT so'rovi yuboramiz .
        """
        task = get_object_or_404(Task, pk=pk, user=request.user)# Berilgan ID bo'yicha taskni olamiz 
        serializer = TaskSerializer(task, data=request.data, partial=True)  # Taskni yangilash uchun serializerni yaratib olamiz.partial=True qo'yishimdan maqsad  serializer faqat berilgan maydonlar bo'yicha yangilashni amalga oshiradi. Agar foydalanuvchi faqat bir nechta maydonlarni (masalan, faqat title yoki description) yangilashni xohlasa, unga boshqa maydonlarni ko'rsatmaymiz . Bu qo'shimcha ma'lumotlarni kiritmasdan yangilanishni ta'minlaydi.
        # qolganlari ham shu ketma ketlikda amalga oshiriladi
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Taskni o'chirish uchun DELETE so'rovi yuboramiz.
        """
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Special Task API
class SpecialTaskAPIView(APIView):
    # JWT autentifikatsiyasi va IsAuthenticated talabini bu qismga ham qoyamiz 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Maxsus sana bo'yicha SpecialTasklar ro'yxatini olish uchun GET so'rovi yuboramiz.
        """
        special_date = request.query_params.get('special_date')
        tasks = SpecialTask.objects.filter(user=request.user)

        if special_date:
            tasks = tasks.filter(special_date=special_date)

        serializer = SpecialTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Yangi SpecialTask yaratish uchun POST so'rovi yuboramiz.
        """
        serializer = SpecialTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        SpecialTaskni yangilash uchun PUT so'rovi yuboramiz.
        """
        task = get_object_or_404(SpecialTask, pk=pk, user=request.user)
        serializer = SpecialTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        SpecialTaskni o'chirish uchun DELETE so'rovi yuboramiz.
        """
        task = get_object_or_404(SpecialTask, pk=pk, user=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
