from rest_framework import serializers

from products.models.product import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
