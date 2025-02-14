from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import filter_by_language, translate_and_store

from .models import Service, ServiceImage
from .serializers import ServiceSerializer


class ServiceListUserAPI(APIView):
    """🚀 Foydalanuvchilar uchun xizmatlar ro‘yxati"""

    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        status_filter = request.query_params.get("status", "faol")

        services = Service.objects.filter(status=status_filter)

        services = filter_by_language(
            services,
            lang,
            {
                "name": ("name_uz", "name_ru"),
                "description": ("description_uz", "description_ru"),
            },
        )

        serializer = ServiceSerializer(services, many=True, context={"lang": lang})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceAdminAPI(APIView):
    """🚀 Admin uchun xizmatlar CRUD API"""

    def get(self, request, pk=None):
        if pk is None:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data)

        service = get_object_or_404(Service, pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()

            # ✅ Tarjima qo‘shish
            translate_and_store(
                service,
                [
                    ("name_uz", "name_ru"),
                    ("description_uz", "description_ru"),
                ],
            )

            # ✅ Agar rasmlar bo‘lsa, yuklash
            images = request.FILES.getlist("images")
            for image in images:
                ServiceImage.objects.create(service=service, image=image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        service = get_object_or_404(Service, pk=pk)

        # ✅ Foydalanuvchi yuborgan status ma'lumotini olish
        status_value = request.data.get("status", None)
        if status_value:
            service.status = status_value

        # ✅ Boshqa maydonlarni yangilash
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
