from django.urls import path

from .views import TestAttributeAPIView, TestFilterAPI, TestTranslateAPI

urlpatterns = [
    path(
        "api/test/attributes/", TestAttributeAPIView.as_view(), name="test-attributes"
    ),
    path("api/test/translate/", TestTranslateAPI.as_view(), name="test-translate"),
    path("api/test/filter/", TestFilterAPI.as_view(), name="test-filter"),
]
