from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import (
    apply_currency_conversion,
    filter_by_language,
    get_conversion_rates,
)
from DesktopFPSGames.desktop_serializers import DesktopSerializer
from DesktopFPSGames.models1.desktop import Desktop


class DesktopListUserAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        currency = request.query_params.get("currency", "uzs")
        type_id = request.query_params.get("type")
        status_filter = request.query_params.get("status", "faol")
        rates = get_conversion_rates()

        queryset = Desktop.objects.prefetch_related("type", "attributes", "images")

        # **Kategoriya bo‘yicha filter qollaymiz**
        if type_id:
            queryset = queryset.filter(type=type_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # **Til bo‘yicha filter qollaymzi**
        queryset = filter_by_language(
            queryset,
            lang,
            {
                "name": ("name_uz", "name_ru"),
                "description": ("description_uz", "description_ru"),
                "type_name": ("type__name_uz", "type__name_ru"),
            },
        )

        # **Valyutani konvertatsiya qilish qismi**
        queryset = apply_currency_conversion(queryset, currency, rates)

        serializer = DesktopSerializer(
            queryset, many=True, context={"lang": lang, "request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class DesktopDetailUserAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            desktop = Desktop.objects.prefetch_related(
                "type", "attributes", "images"
            ).get(pk=pk)
            lang = request.query_params.get("lang", None)
            currency = request.query_params.get("currency", None)

            serializer = DesktopSerializer(
                desktop, context={"lang": lang, "currency": currency}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Desktop.DoesNotExist:
            return Response(
                {"error": "Desktop topilmadi yoki yaratilmagan "},
                status=status.HTTP_404_NOT_FOUND,
            )
