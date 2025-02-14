from django.urls import path

from .views import BannerAdminAPI, BannerListUserAPI

urlpatterns = [
    # Foydalanuvchilar uchun bannerlar ro'yxati olish uchun
    path("api/users/banners/", BannerListUserAPI.as_view(), name="banner-list-user"),
    # Admin uchun bannerlar yaratish
    path("api/admin/banners/", BannerAdminAPI.as_view(), name="banner-admin"),
    # Admin uchun bannerni ID bo‘yicha olish, o‘zgartirish yoki o‘chirish uchun
    path(
        "api/admin/banners/<int:pk>/",
        BannerAdminAPI.as_view(),
        name="banner-admin-detail",
    ),
]
