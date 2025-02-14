from django.urls import path

from order_and_zayavka.views.delivery_method import (
    AdminDeliveryPriceAPI,
    AdminDeliveryPriceDetailAPI,
    AdminDistrictAPI,
    AdminDistrictDetailAPI,
    AdminPickupPointAPI,
    AdminPickupPointDetailAPI,
    AdminRegionAPI,
    AdminRegionDetailAPI,
)
from order_and_zayavka.views.order import (
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
from order_and_zayavka.views.zayafka import AdminZayafkaAPI

urlpatterns = [
    #  Admin APIs
    path("api/admin/orders/", AdminOrderAPI.as_view(), name="admin-orders"),
    path(
        "api/admin/orders/<int:id>/",
        AdminOrderDetailAPI.as_view(),
        name="admin-order-detail",
    ),
    path(
        "api/admin/orders/<int:id>/patch/",
        AdminOrderAPI.as_view(),
        name="admin-order-update",
    ),
    path("api/admin/zayafka/", AdminZayafkaAPI.as_view(), name="admin-zayafka"),
    #  User APIs
    path("api/users/zayafka/", UserZayafkaAPI.as_view(), name="user-zayafka"),
    path("api/users/order/", UserOrderAPI.as_view(), name="user-order"),
    path("api/users/comments/", UserCommentsAPI.as_view(), name="user-comments"),
    path("api/admin/region/", AdminRegionAPI.as_view(), name="admin-region"),
    path(
        "api/admin/region/<int:pk>/",
        AdminRegionDetailAPI.as_view(),
        name="admin-region-detail",
    ),
    path("api/admin/district/", AdminDistrictAPI.as_view(), name="admin-district"),
    path(
        "api/admin/district/<int:pk>/",
        AdminDistrictDetailAPI.as_view(),
        name="admin-district-detail",
    ),
    path("api/admin/pickup_point/", AdminPickupPointAPI.as_view(), name="admin-pickup"),
    path(
        "api/admin/pickup_point/<int:pk>/",
        AdminPickupPointDetailAPI.as_view(),
        name="admin-pickup-detail",
    ),
    path(
        "api/admin/delivery_price/", AdminDeliveryPriceAPI.as_view(), name="admin-price"
    ),
    path(
        "api/admin/delivery_price/<int:pk>/",
        AdminDeliveryPriceDetailAPI.as_view(),
        name="admin-price-detail",
    ),
    #  Olib ketish opsiyalarini olish
    path(
        "api/users/pickup_points/",
        UserPickupPointsAPI.as_view(),
        name="user-pickup-points",
    ),
    #  Yetkazib berish opsiyalarini olish
    path(
        "api/users/delivery_price/",
        UserDeliveryPriceAPI.as_view(),
        name="user-delivery-price",
    ),
    # Olib ketish buyurtmasi qilish
    path(
        "api/users/pickup_order/",
        UserPickupOrderAPI.as_view(),
        name="user-pickup-order",
    ),
    #  Yetkazib berish buyurtmasi qilish
    path(
        "api/users/delivery_order/",
        UserDeliveryOrderAPI.as_view(),
        name="user-delivery-order",
    ),
    path(
        "api/users/detect-region/",
        UserRegionDetectAPI.as_view(),
        name="user-detect-region",
    ),
]
