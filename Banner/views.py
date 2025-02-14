from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import filter_by_language, translate_and_store

from .models import Banner
from .serializers import BannerSerializer


class BannerListUserAPI(APIView):
    """Foydalanuvchilar uchun bannerlar ro‘yxati oladigan qismi"""

    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        status_filter = request.query_params.get("status", "faol")

        banners = Banner.objects.filter(status=status_filter)

        # Tilga mos bannerlarni olish uchun utilsdan logikani chqirib olamiz
        banners = filter_by_language(
            banners,
            lang,
            {
                "name": ("name_uz", "name_ru"),
                "description": ("description_uz", "description_ru"),
            },
        )

        serializer = BannerSerializer(banners, many=True, context={"lang": lang})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BannerAdminAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """Admin uchun bannerlarni CRUD     qilish"""

    def get(self, request, pk=None):
        """Bannerlarni ro'yxati yoki bitta banner olafigan logika"""
        if pk is None:
            banners = Banner.objects.all()
            serializer = BannerSerializer(banners, many=True)
            return Response(serializer.data)
        try:
            banner = Banner.objects.get(pk=pk)
            serializer = BannerSerializer(banner)
            return Response(serializer.data)
        except Banner.DoesNotExist:
            return Response(
                {"error": "Banner topilmaid  yoki hali yaratilmagan!"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        """Yangi banner yaratish"""
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            banner = serializer.save()
            translate_and_store(
                banner, [("name_uz", "name_ru"), ("description_uz", "description_ru")]
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Mavjud bannerni yangilash"""
        try:
            banner = Banner.objects.get(pk=pk)
        except Banner.DoesNotExist:
            return Response(
                {"error": "Banner not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BannerSerializer(banner, data=request.data, partial=True)
        if serializer.is_valid():
            banner = serializer.save()
            translate_and_store(
                banner,
                {
                    "name": ("name_uz", "name_ru"),
                    "description": ("description_uz", "description_ru"),
                },
            )

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Bannerni o‘chirish"""
        try:
            banner = Banner.objects.get(pk=pk)
        except Banner.DoesNotExist:
            return Response(
                {"error": "Banner not found"}, status=status.HTTP_404_NOT_FOUND
            )

        banner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
