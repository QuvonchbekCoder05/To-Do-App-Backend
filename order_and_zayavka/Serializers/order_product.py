from rest_framework import serializers

from order_and_zayavka.models.order_product import OrderProduct
from order_and_zayavka.Serializers.productDetailSerializer import (
    ProductDetailSerializer,
)


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer()

    class Meta:
        model = OrderProduct
        fields = "__all__"
