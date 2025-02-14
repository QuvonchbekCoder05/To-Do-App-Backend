"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="My API files",
        default_version="v1",
        description="IngameUZ API hujjatlari",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path("adminuser/", include("adminuser.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("orderz/", include("order_and_zayavka.urls")),
    path("products/", include("products.urls")),
    path("desktop/", include("DesktopFPSGames.urls")),
    path("banner/", include("Banner.urls")),
    path("service/", include("Service.urls")),
    path("news/", include("News.urls")),
    path("discount/", include("Discount.urls")),
    path("search/", include("search.urls")),
    path("test/", include("translation_test.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
