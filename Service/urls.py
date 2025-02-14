from django.urls import path

from .views import ServiceAdminAPI, ServiceListUserAPI

urlpatterns = [
    path("api/users/services/", ServiceListUserAPI.as_view(), name="service-list-user"),
    path("api/admin/services/", ServiceAdminAPI.as_view(), name="service-admin"),
    path(
        "api/admin/services/<int:pk>/",
        ServiceAdminAPI.as_view(),
        name="service-admin-detail",
    ),
]
