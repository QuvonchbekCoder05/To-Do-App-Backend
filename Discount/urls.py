from django.urls import path

from .views import DiscountAdminAPI, DiscountListAPI

urlpatterns = [
    path("discounts/", DiscountListAPI.as_view(), name="discount-list"),
    path("admin/discounts/", DiscountAdminAPI.as_view(), name="admin-discount"),
    path(
        "admin/discounts/<int:pk>/",
        DiscountAdminAPI.as_view(),
        name="admin-discount-detail",
    ),
]
