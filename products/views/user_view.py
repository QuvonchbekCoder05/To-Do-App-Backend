from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import (
    apply_currency_conversion,
    filter_by_language,
    get_conversion_rates,
    translate_and_store,
)
from products.models.category import Category
from products.models.product import Product
from products.serializers.category_serializer import CategorySerializer


class CategoryGetAPIView(APIView):
    def get(self, request, id=None):
        lang = request.query_params.get("lang", "uz")
        queryset = Category.objects.all()

        if lang == "uz":
            result = queryset.values("id", "name_uz")
        elif lang == "ru":
            result = queryset.values("id", "name_ru")
        else:
            result = queryset.values("id", "name_uz")  # Default - Uzbekcha qilamiz

        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            translate_and_store(category, [("name_uz", "name_ru")])  # Tarjima qilish
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProductAPIView(APIView):
    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        category_id = request.query_params.get("category")
        currency = request.query_params.get("currency", "uzs")
        status_filter = request.query_params.get("status", "faol")

        rates = get_conversion_rates()
        queryset = Product.objects.prefetch_related(
            "category", "brand", "type", "attributes"
        )

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if category_id:
            queryset = queryset.filter(category=category_id)

        queryset = filter_by_language(
            queryset,
            lang,
            {
                "name": ("name_uz", "name_ru"),
                "description": ("description_uz", "description_ru"),
                "category_name": ("category__name_uz", "category__name_ru"),
                "type_name": ("type__name_uz", "type__name_ru"),
            },
        )

        queryset = apply_currency_conversion(queryset, currency, rates)

        return Response(
            self.serialize_products(queryset, lang), status=status.HTTP_200_OK
        )

    def serialize_products(self, queryset, lang):
        return [
            {
                "id": p.id,
                "category": p.category.id,
                "brand": p.brand.id,
                "type": p.type.id,
                "attributes": [a.id for a in p.attributes.all()],
                "category_detail": {
                    "id": p.category.id,
                    "name": p.category_name,
                },
                "brand_detail": {
                    "id": p.brand.id,
                    "name": p.brand.name,
                },
                "type_detail": {
                    "id": p.type.id,
                    "name": p.type_name,
                },
                "attributes_detail": {
                    (a.key_uz if lang == "uz" else a.key_ru): (
                        a.value_uz if lang == "uz" else a.value_ru
                    )
                    for a in p.attributes.all()
                    if (a.key_uz if lang == "uz" else a.key_ru)
                },
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "status": p.status,
                "images": p.images.url if p.images else None,
                "slug": p.slug,
                "converted_price": getattr(p, "converted_price", p.price),
            }
            for p in queryset
        ]
