from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import filter_by_language, translate_and_store

from .models import News
from .serializers import NewsSerializer


class NewsAdminAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """📢 Adminlar uchun yangiliklarni boshqarish"""

    def get(self, request, pk=None):
        """📰 Bitta yoki barcha yangiliklarni olish"""
        if pk is not None:
            news = News.objects.filter(pk=pk).first()
            if not news:
                return Response(
                    {"error": "News topilmadi"}, status=status.HTTP_404_NOT_FOUND
                )
            return Response(NewsSerializer(news).data, status=status.HTTP_200_OK)

        news_list = News.objects.all()
        return Response(
            NewsSerializer(news_list, many=True).data, status=status.HTTP_200_OK
        )

    def post(self, request):
        """🆕 Yangi yangilik qo‘shish"""
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.save()
            translate_and_store(
                news, [("name_uz", "name_ru"), ("description_uz", "description_ru")]
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """✏️ Yangilikni yangilash"""
        news = News.objects.filter(pk=pk).first()
        if not news:
            return Response(
                {"error": "News topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = NewsSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            news = serializer.save()
            translate_and_store(
                news, [("name_uz", "name_ru"), ("description_uz", "description_ru")]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """🗑 Yangilikni o‘chirish"""
        news = News.objects.filter(pk=pk).first()
        if not news:
            return Response(
                {"error": "News topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        news.delete()
        return Response(
            {"message": "News o‘chirildi"}, status=status.HTTP_204_NO_CONTENT
        )


class NewsListUserAPI(APIView):
    """👥 Foydalanuvchilar uchun yangiliklar ro‘yxati"""

    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        status_filter = request.query_params.get("status", "faol")

        news = News.objects.filter(status=status_filter)

        # 🔄 Til bo‘yicha filter
        news = filter_by_language(
            news,
            lang,
            {
                "name": ("name_uz", "name_ru"),
                "description": ("description_uz", "description_ru"),
            },
        )

        serializer = NewsSerializer(news, many=True, context={"lang": lang})
        return Response(serializer.data, status=status.HTTP_200_OK)
