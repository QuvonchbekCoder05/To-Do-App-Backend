# views/__init__.py
from order_and_zayavka.views.core import (
    APIView,
    JSONParser,
    Response,
    serializers,
    status,
)

from .delivery_method import (
    AdminDeliveryPriceAPI,
    AdminDeliveryPriceDetailAPI,
    AdminDistrictAPI,
    AdminDistrictDetailAPI,
    AdminPickupPointAPI,
    AdminPickupPointDetailAPI,
    AdminRegionAPI,
    AdminRegionDetailAPI,
)
from .order import (
    AdminOrderAPI,
    AdminOrderDetailAPI,
    UserCommentsAPI,
    UserDeliveryOrderAPI,
    UserDeliveryPriceAPI,
    UserOrderAPI,
    UserPickupOrderAPI,
    UserPickupPointsAPI,
    UserRegionDetectAPI,
    UserZayafkaAPI,
)
from .zayafka import AdminZayafkaAPI
