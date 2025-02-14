from rest_framework import serializers

from products.models.attribute import Attribute


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["id", "key_uz", "key_ru", "value_uz", "value_ru"]
