# serializers/__init__.py
from order_and_zayavka.Serializers.delivery_method import (
    DeliveryAddressSerializer,
    DeliveryPriceSerializer,
    DistrictSerializer,
    PickupPointSerializer,
    RegionSerializer,
)
from order_and_zayavka.Serializers.order import OrderSerializer
from order_and_zayavka.Serializers.order_product import OrderProductSerializer
from order_and_zayavka.Serializers.zayafka import ZayafkaSerializer
