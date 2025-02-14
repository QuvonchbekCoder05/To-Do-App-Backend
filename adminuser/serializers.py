from rest_framework import serializers

from .models import SiteVisitor


class SiteVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteVisitor
        fields = "__all__"
