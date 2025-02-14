from rest_framework import serializers

from products.models.conversion import Conversion


class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversion
        fields = "__all__"
