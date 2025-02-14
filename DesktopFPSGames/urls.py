from django.urls import path

from .views1.admin_views import (
    DesktopAdminAPI,
    DesktopAttributesAdminAPI,
    DesktopTypeAdminAPI,
)
from .views1.user_views import DesktopDetailUserAPI, DesktopListUserAPI

urlpatterns = [
    # ✅ **Admin API qismi**
    path("admin/desktop/", DesktopAdminAPI.as_view(), name="admin-desktop-list"),
    path(
        "admin/desktop/<int:pk>/",
        DesktopAdminAPI.as_view(),
        name="admin-desktop-detail",
    ),
    path(
        "admin/desktop_type/", DesktopTypeAdminAPI.as_view(), name="admin-desktop-type"
    ),
    path(
        "admin/desktop_type/<int:pk>/",
        DesktopTypeAdminAPI.as_view(),
        name="admin-desktop-type-detail",
    ),
    path(
        "admin/desktop_attributes/",
        DesktopAttributesAdminAPI.as_view(),
        name="admin-desktop-attributes",
    ),
    path(
        "admin/desktop_attributes/<int:pk>/",
        DesktopAttributesAdminAPI.as_view(),
        name="admin-desktop-attributes-detail",
    ),
    # ✅ **User API qismi**
    path("users/desktop/", DesktopListUserAPI.as_view(), name="user-desktop-list"),
    path(
        "users/desktop/<int:pk>/",
        DesktopDetailUserAPI.as_view(),
        name="user-desktop-detail",
    ),
]
