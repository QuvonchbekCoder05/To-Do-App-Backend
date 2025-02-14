from rest_framework import serializers

from .models import Service, ServiceImage


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ["id", "image"]


class ServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)

    class Meta:
        model = Service
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
        """✅ Foydalanuvchiga tilga mos ma'lumot chiqarish"""
        representation = super().to_representation(instance)
        lang = self.context.get("lang", "uz")

        if lang == "uz":
            representation.pop("name_ru", None)
            representation.pop("description_ru", None)
        elif lang == "ru":
            representation.pop("name_uz", None)
            representation.pop("description_uz", None)

        return representation
