from django.urls import path

from .views import NewsAdminAPI, NewsListUserAPI

urlpatterns = [
    path("admin/news/", NewsAdminAPI.as_view(), name="admin-news-list"),
    path("admin/news/<int:pk>/", NewsAdminAPI.as_view(), name="admin-news-detail"),
    path("users/news/", NewsListUserAPI.as_view(), name="service-list-user"),
]
