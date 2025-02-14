from django.urls import path

from products.views.attribute_view import AttributeAPIView
from products.views.brand_view import BrandAPIView
from products.views.category_view import CategoryListCreateAPIView
from products.views.conversion_view import ConversionAPIView
from products.views.product_view import ProductAPIView
from products.views.type_view import TypeListCreateAPIView
from products.views.user_view import CategoryGetAPIView, UserProductAPIView

urlpatterns = [
    #  Admin API'lari (CRUD)
    path("admin/conversion/", ConversionAPIView.as_view(), name="admin-conversion"),
    path("conversion/<int:pk>/", ConversionAPIView.as_view(), name="conversion_detail"),
    path(
        "admin/categories/<int:pk>/",  # Specific category ID
        CategoryListCreateAPIView.as_view(),
        name="admin-category-detail",
    ),
    path(
        "admin/categories/",  # All categories
        CategoryListCreateAPIView.as_view(),
        name="admin-category-list",
    ),
    path("admin/brands/", BrandAPIView.as_view(), name="admin-brands"),
    path(
        "brands/<int:id>/", BrandAPIView.as_view(), name="brand-retrieve-update-delete"
    ),
    path("admin/products/", ProductAPIView.as_view(), name="admin-products"),
    path(
        "products/<int:id>/",
        ProductAPIView.as_view(),
        name="product-retrieve-update-delete",
    ),
    path("admin/attributes/", AttributeAPIView.as_view(), name="admin-attributes"),
    path(
        "attributes/<int:id>/",
        AttributeAPIView.as_view(),
        name="attribute-retrieve-update-delete",
    ),
    path("admin/types/", TypeListCreateAPIView.as_view(), name="admin-types"),
    path(
        "types/<int:id>/",
        TypeListCreateAPIView.as_view(),
        name="type-retrieve-update-delete",
    ),
    # Foydalanuvchi API'lari (GET bilan filterlash)
    path("user/products/", UserProductAPIView.as_view(), name="user-products"),
    path("user/category/", CategoryGetAPIView.as_view(), name="user-category"),
]
