from rest_framework import serializers

from order_and_zayavka.models.delivery_method import District, PickupPoint, Region
from order_and_zayavka.models.order import Order
from order_and_zayavka.models.order_product import OrderProduct
from products.serializers.product_serializer import (  # ✅ Mahsulot uchun serializer
    ProductSerializer,
)


class PickupPointSerializer(serializers.ModelSerializer):
    """🚗 Olib ketish punktlari serializeri"""

    class Meta:
        model = PickupPoint
        fields = ["id", "address_uz", "address_ru", "latitude", "longitude", "district"]


class OrderProductSerializer(serializers.ModelSerializer):
    """🛒 Buyurtmadagi mahsulotlar to‘liq chiqishi uchun serializer"""

    product = ProductSerializer(read_only=True)  # ✅ ID emas, to‘liq ma'lumot qaytaradi

    class Meta:
        model = OrderProduct
        fields = ["id", "product", "quantity"]  # ✅ Mahsulot to‘liq chiqishi uchun


class OrderSerializer(serializers.ModelSerializer):
    """📦 Buyurtma serializeri"""

    delivery_pickup_point = serializers.PrimaryKeyRelatedField(
        queryset=PickupPoint.objects.all(), required=False, allow_null=True
    )  # ✅ ID sifatida qabul qiladi (o‘z holicha qoladi)

    delivery_pickup_point_detail = PickupPointSerializer(
        source="delivery_pickup_point", read_only=True
    )  # ✅ Faqat GET uchun obyekt shaklida qaytariladi

    delivery_region = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), required=False
    )
    delivery_district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(), required=False
    )
    delivery_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )

    products = OrderProductSerializer(
        source="orderproduct_set", many=True, read_only=True
    )  # ✅ To‘liq mahsulot ma'lumotlari chiqadi

    class Meta:
        model = Order
        fields = "__all__"
