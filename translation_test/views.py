from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import filter_by_language, translate_text

from .models import TestAttribute
from .serializers import TestAttributeSerializer


class TestAttributeAPIView(APIView):
    """Test uchun Attribute API yaratamiz"""

    def get(self, request):
        lang = request.query_params.get("lang", "uz")  # Uz yoki Ru
        attributes = TestAttribute.objects.all()

        # filter_by_language dan foydalandik!
        attributes = filter_by_language(
            attributes,
            lang,
            {"key": ("key_uz", "key_ru"), "value": ("value_uz", "value_ru")},
        )

        serializer = TestAttributeSerializer(attributes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Yangi test attribute qo‘shish"""
        serializer = TestAttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestTranslateAPI(APIView):
    """Google Translate to‘g‘ri ishlayotganini tekshirish API"""

    def get(self, request):
        text = request.query_params.get("text", "")
        lang = request.query_params.get("lang", "uz")

        translated_text = translate_text(text, lang)

        return Response({"translated_text": translated_text}, status=status.HTTP_200_OK)


class TestFilterAPI(APIView):
    """filter_by_language to‘g‘ri ishlayotganini tekshirish API"""

    def get(self, request):
        lang = request.query_params.get("lang", "uz")

        attributes = TestAttribute.objects.all()
        attributes = filter_by_language(
            attributes,
            lang,
            {"key": ("key_uz", "key_ru"), "value": ("value_uz", "value_ru")},
        )

        serializer = TestAttributeSerializer(attributes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
