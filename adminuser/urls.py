from django.urls import path

from .views import (
    AdminLoginAPI,
    AdminLogoutAPI,
    AdminOrderFilterAPI,
    AdminUserDetailAPI,
    AdminUserListAPI,
)

urlpatterns = [
    path("api/admin/login/", AdminLoginAPI.as_view(), name="admin-login"),
    path("api/admin/logout/", AdminLogoutAPI.as_view(), name="admin-logout"),
    path("api/admin/users/", AdminUserListAPI.as_view(), name="admin-users"),
    path(
        "api/admin/users/<int:id>/",
        AdminUserDetailAPI.as_view(),
        name="admin-user-detail",
    ),
    path(
        "status/admin/orders/",
        AdminOrderFilterAPI.as_view(),
        name="admin-orders-filter",
    ),
]
