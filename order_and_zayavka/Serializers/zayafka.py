from rest_framework import serializers

from order_and_zayavka.models.Zayafka import Zayafka


# Zayavka serializer
class ZayafkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zayafka
        fields = "__all__"
