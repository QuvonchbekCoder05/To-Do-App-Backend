from decimal import Decimal

import requests
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product

from .models import Discount


class DiscountListAPI(APIView):
    """Foydalanuvchilar uchun chegirma qilingan mahsulotlar qaytaradigan logika"""

    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        category = request.query_params.get("category", None)
        currency = request.query_params.get("currency", "usd")

        # **Mahsulotlarni `products` API dan olamiz **
        products_api_url = "http://127.0.0.1:8000/products/user/products/"
        params = {
            "lang": lang,
            "category": category,
            "currency": currency,
            "status": "discounted",  # **Faqat chegirmali mahsulotlarni olamiz **
        }
        response = requests.get(products_api_url, params=params)

        if response.status_code != 200:
            return Response(
                {"error": "Mahsulotlar olinmadi yoki yaratilmagan "},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        products_data = response.json()

        # **Mahsulot ID larini `Discount` jadvalidan olamiz **
        discounted_products = {d.product.id: d for d in Discount.objects.all()}

        # **Chegirmali mahsulotlarni hisoblash logikasi**
        for product in products_data:
            product_id = product["id"]
            if product_id in discounted_products:
                discount = discounted_products[product_id]

                discount_amount = (
                    Decimal(product["price"]) * discount.discount_percent
                ) / Decimal(100)
                product["discount_price"] = round(
                    Decimal(product["price"]) - discount_amount, 2
                )
                product["discount"] = f"{discount.discount_percent}%"

        return Response(products_data, status=status.HTTP_200_OK)


class DiscountAdminAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """Admin uchun mahsulotga chegirma qo‘shish va olib tashlash"""

    def post(self, request):
        product_id = request.data.get("product_id")
        discount_percent = request.data.get("discount_percent")

        # **Agar discount_percent berilmasa, xato qaytarish**
        if discount_percent is None:
            return Response(
                {"error": "discount_percent maydoni talab qilinadi"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # **Mahsulot `products` API'dan olinadi**
        products_api_url = f"http://127.0.0.1:8000/products/products/{product_id}/"
        response = requests.get(products_api_url)

        if response.status_code != 200:
            return Response(
                {"error": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        # **Mahsulot mavjudligini Product modelidan tekshiramiz**
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Mahsulot topilmadi (Product Model)"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # **Mahsulotga chegirma qo‘shish**
        discount, created = Discount.objects.get_or_create(
            product=product, defaults={"discount_percent": discount_percent}
        )

        # **Agar obyekt avvaldan mavjud bo‘lsa, yangi chegirma qiymatini saqlaymiz**
        if not created:
            discount.discount_percent = discount_percent
            discount.save()

        # **Mahsulotni `discounted` statusga o‘tkazish**
        requests.put(products_api_url, json={"status": "discounted"})

        return Response(
            {"message": "Mahsulotga chegirma qo‘shildi"}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        try:
            discount = Discount.objects.get(pk=pk)
            product_id = discount.product.id
            discount.delete()

            # **Mahsulotni `active` statusga qaytarish**
            products_api_url = f"http://127.0.0.1:8000/products/products/{product_id}/"
            requests.put(products_api_url, json={"status": "active"})

            return Response(
                {"message": "Chegirma olib tashlandi"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Discount.DoesNotExist:
            return Response(
                {"error": "Chegirma topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )
