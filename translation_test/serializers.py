from rest_framework import serializers

from .models import TestAttribute


class TestAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAttribute
        fields = "__all__"
