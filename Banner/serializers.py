from rest_framework import serializers

from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            "id",
            "name_uz",
            "name_ru",
            "description_uz",
            "description_ru",
            "image",
            "url",
            "status",
            "slug",
        ]
        extra_kwargs = {"slug": {"read_only": True}}

    def to_representation(self, instance):
        """Lang parametriga qarab mos maydonlarni qaytarish uchun logika"""
        representation = super().to_representation(instance)
        lang = self.context.get("lang", "uz")

        if lang == "uz":
            representation.pop("name_ru", None)
            representation.pop("description_ru", None)
        elif lang == "ru":
            representation.pop("name_uz", None)
            representation.pop("description_uz", None)

        return representation
