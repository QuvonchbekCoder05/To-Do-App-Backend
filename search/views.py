from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import filter_by_language
from DesktopFPSGames.models1.desktop import Desktop
from products.models.product import Product
from Service.models import Service


class SearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class SearchAPI(APIView):
    def get(self, request):
        search_query = request.query_params.get("search", "")
        lang = request.query_params.get("lang", "uz")

        if not search_query:
            return Response(
                {"error": "Qidiruv so‘rovi bo‘sh bo‘lishi mumkin emas"}, status=400
            )

        # **Mahsulotlar bo‘yicha qidirish**
        products = Product.objects.filter(
            Q(name_uz__icontains=search_query)
            | Q(name_ru__icontains=search_query)
            | Q(description_uz__icontains=search_query)
            | Q(description_ru__icontains=search_query)
        )
        products = filter_by_language(
            products,
            lang,
            {
                "name": ("name_uz", "name_ru"),
                "description": ("description_uz", "description_ru"),
            },
        )

        # **Kompyuterlar bo‘yicha qidirish**
        desktops = Desktop.objects.filter(
            Q(name_uz__icontains=search_query)
            | Q(name_ru__icontains=search_query)
            | Q(description_uz__icontains=search_query)
            | Q(description_ru__icontains=search_query)
        )
        desktops = filter_by_language(
            desktops,
            lang,
            {
                "name": ("name_uz", "name_ru"),
                "description": ("description_uz", "description_ru"),
            },
        )

        #  **Xizmatlar bo‘yicha qidirish**
        services = Service.objects.filter(
            Q(name_uz__icontains=search_query)
            | Q(name_ru__icontains=search_query)
            | Q(description_uz__icontains=search_query)
            | Q(description_ru__icontains=search_query)
        )
        services = filter_by_language(
            services,
            lang,
            {
                "name": ("name_uz", "name_ru"),
                "description": ("description_uz", "description_ru"),
            },
        )

        all_results = list(products) + list(desktops) + list(services)

        all_results.sort(
            key=lambda obj: search_query.lower() in obj.name.lower(), reverse=True
        )

        # **Pagination qo‘shamiz mashtablashtirish uchun **
        paginator = SearchPagination()
        paginated_results = paginator.paginate_queryset(all_results, request)

        #  **Natijalarni JSON formatga o‘tkazamiz **
        results = [
            {
                "id": obj.id,
                "type": obj.__class__.__name__,
                "name": obj.name,
                "description": obj.description,
                "price": getattr(obj, "price", None),
                "status": getattr(obj, "status", None),
                "images": obj.images.url
                if hasattr(obj, "images") and obj.images
                else None,
                "slug": getattr(obj, "slug", None),
            }
            for obj in paginated_results
        ]

        return paginator.get_paginated_response(results)
