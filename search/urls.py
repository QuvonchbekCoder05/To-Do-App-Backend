from django.urls import path

from .views import SearchAPI

urlpatterns = [
    path("api/search/", SearchAPI.as_view(), name="search-api"),
]
