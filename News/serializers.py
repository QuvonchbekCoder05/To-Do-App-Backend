from rest_framework import serializers

from .models import Image, News


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image"]


class NewsSerializer(serializers.ModelSerializer):
    images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "description_uz",
            "description_ru",
            "status",
            "slug",
            "images",
        ]

    def to_representation(self, instance):
        """🌍 Til bo‘yicha filter"""
        representation = super().to_representation(instance)
        lang = self.context.get("lang", "uz")

        if lang == "uz":
            representation.pop("name_ru", None)
            representation.pop("description_ru", None)
        elif lang == "ru":
            representation.pop("name_uz", None)
            representation.pop("description_uz", None)

        return representation
