from rest_framework import serializers

from order_and_zayavka.models.delivery_method import (
    DeliveryAddress,
    DeliveryPrice,
    District,
    PickupPoint,
    Region,
)


# ✅ Viloyat serializer
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lang = self.context.get("lang", "uz")  # Langni kontekstdan olamiz

        if lang == "uz":
            representation.pop("name_ru", None)  #  Ruscha maydonni olib tashlaymiz
        elif lang == "ru":
            representation.pop("name_uz", None)  # O‘zbekcha maydonni olib tashlaymiz

        return representation


# ✅ Tuman serializer
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lang = self.context.get("lang", "uz")

        if lang == "uz":
            representation.pop("name_ru", None)
        elif lang == "ru":
            representation.pop("name_uz", None)

        return representation


# ✅ Olib ketish punktlari uchun  serializer
class PickupPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupPoint
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lang = self.context.get("lang", "uz")

        if lang == "uz":
            representation.pop("address_ru", None)
        elif lang == "ru":
            representation.pop("address_uz", None)

        return representation


# ✅ Yetkazib berish narxlari  uchun serializer
class DeliveryPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPrice
        fields = "__all__"


# ✅ Yetkazib berish manzillari uchun serializer
class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = "__all__"
