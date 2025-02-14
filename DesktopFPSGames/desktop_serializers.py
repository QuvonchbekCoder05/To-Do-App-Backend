from decimal import Decimal

from rest_framework import serializers

from config.utils import get_conversion_rates
from DesktopFPSGames.models1.attributes import DesktopAttributes
from DesktopFPSGames.models1.desktop import Desktop
from DesktopFPSGames.models1.desktop_type import DesktopType


class DesktopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesktopType
        fields = ["id", "name_uz", "name_ru", "slug"]


class DesktopAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesktopAttributes
        fields = ["id", "key_uz", "key_ru", "value_uz", "value_ru"]


class DesktopSerializer(serializers.ModelSerializer):
    type_detail = DesktopTypeSerializer(source="type", read_only=True)
    images = serializers.SerializerMethodField()
    attributes_detail = serializers.SerializerMethodField()
    converted_price = serializers.SerializerMethodField()

    class Meta:
        model = Desktop
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "description_uz",
            "description_ru",
            "price",
            "status",
            "slug",
            "images",
            "converted_price",
            "type",
            "type_detail",
            "attributes_detail",
        ]

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    def get_converted_price(self, obj):
        """Valyutani foydalanuvchi tanlagan kursga o‘tkazish logikasi"""
        request = self.context.get("request")  #  Request object olamzi id emas

        if not request or not hasattr(request, "query_params"):
            return obj.price

        currency = request.query_params.get(
            "currency", "uzs"
        )  #  So‘rovdan currency olamoz
        rates = get_conversion_rates()

        if currency == "uzs":
            return round(Decimal(obj.price) * rates["usd_to_uzs"], 2)
        elif currency == "usd":
            return round(Decimal(obj.price) * rates["uzs_to_usd"], 2)
        return obj.price

    def get_attributes_detail(self, obj):
        lang = self.context.get("lang", "uz")
        attributes = obj.attributes.all()
        return {
            (attr.key_uz if lang == "uz" else attr.key_ru): (
                attr.value_uz if lang == "uz" else attr.value_ru
            )
            for attr in attributes
            if attr.key_uz
            and attr.key_ru  # Faqat to‘liq ma'lumotlar chiqariladigan qilamiz
        }

    def to_representation(self, instance):
        """Lang parametriga qarab mos maydonlarni qaytaradigan qilamiz"""
        representation = super().to_representation(instance)

        """Ma'lumotni foydalanuvchi so‘rovi bo‘yicha qaytaradigan qila iz"""

        request = self.context.get("request", None)
        self.context["request"] = request

        representation["converted_price"] = self.get_converted_price(instance)

        lang = self.context.get("lang", "uz")

        if lang == "uz":
            representation.pop("name_ru", None)
            representation.pop("description_ru", None)
            if "type_detail" in representation:
                representation["type_detail"].pop("name_ru", None)
        elif lang == "ru":
            representation.pop("name_uz", None)
            representation.pop("description_uz", None)
            if "type_detail" in representation:
                representation["type_detail"].pop("name_uz", None)

        return representation
