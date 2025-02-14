from django.urls import path

from .views import AdminDashboardAPI

urlpatterns = [
    path("api/admin/dashboard/", AdminDashboardAPI.as_view(), name="admin-dashboard"),
]
