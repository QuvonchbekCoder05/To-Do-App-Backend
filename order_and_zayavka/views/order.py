# The provided code includes API views for handling user orders, zayavkas, pickup points, delivery
# prices, comments, and region detection.
import logging

from django.db.models import F
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from config.utils import (
    apply_currency_conversion,
    convert_price,
    filter_by_language,
    get_conversion_rates,
)
from order_and_zayavka.models.delivery_method import DeliveryPrice, PickupPoint, Region
from order_and_zayavka.models.order import Order
from order_and_zayavka.models.order_product import OrderProduct
from order_and_zayavka.Serializers.delivery_method import (
    PickupPointSerializer,
    RegionSerializer,
)
from order_and_zayavka.Serializers.order import OrderSerializer
from order_and_zayavka.Serializers.zayafka import ZayafkaSerializer
from order_and_zayavka.views.core import APIView, Response, status
from products.models.product import Product
from products.serializers.product_serializer import ProductSerializer

logger = logging.getLogger(__name__)


class UserZayafkaAPI(APIView):
    def post(self, request):
        serializer = ZayafkaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Zayavka qoldirildi", "id": serializer.instance.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrderAPI(APIView):
    def post(self, request):
        data = request.data
        products_data = data.pop("products", [])

        pickup_point_id = data.pop("pickup_point", None)
        delivery_region = data.pop("delivery_region", None)

        logger.info(f"📥 Request data: {data}")

        if pickup_point_id:
            try:
                pickup_point = PickupPoint.objects.get(id=pickup_point_id)
                data["delivery_pickup_point"] = pickup_point.id
                logger.info(f"✅ Pickup Point: {pickup_point}")
            except PickupPoint.DoesNotExist:
                return Response({"error": "Pickup Point mavjud emas"}, status=400)

        elif delivery_region:
            data["delivery_region"] = delivery_region

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            logger.info(
                f"Buyurtma saqlandi: ID {order.id}, Pickup Point: {order.delivery_pickup_point}"
            )

            for product_data in products_data:
                product_id = product_data["id"]
                quantity = product_data.get("quantity", 1)
                try:
                    product = Product.objects.get(id=product_id)
                    OrderProduct.objects.create(
                        order=order, product=product, quantity=quantity
                    )
                except Product.DoesNotExist:
                    return Response(
                        {"error": f"Mahsulot ID {product_id} topilmadi"}, status=400
                    )

            return Response({"message": "Order placed", "id": order.id}, status=201)

        return Response(serializer.errors, status=400)


class AdminOrderAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminOrderDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPickupPointsAPI(APIView):

    """Olib ketish punktlarini foydalanuvchi manziliga mos qaytaradigan qilamiz"""

    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        region_id = request.query_params.get("region_id")  # Viloyat ID
        district_id = request.query_params.get("district_id")  #  Tuman ID
        lat = request.query_params.get("lat")  # Latitude (agar xaritadan tanlasa)
        lng = request.query_params.get("lng")  #  Longitude (agar xaritadan tanlasa)

        #  Agar foydalanuvchi VILOYAT yoki TUMAN tanlagan bo‘lsa
        if region_id or district_id:
            pickup_points = PickupPoint.objects.all()
            if region_id:
                pickup_points = pickup_points.filter(district__region_id=region_id)
            if district_id:
                pickup_points = pickup_points.filter(district_id=district_id)

            pickup_points = filter_by_language(
                pickup_points, lang, {"address": ("address_uz", "address_ru")}
            )
            return Response(
                PickupPointSerializer(pickup_points, many=True).data,
                status=status.HTTP_200_OK,
            )

        # Agar foydalanuvchi LAT/LNG jo‘natsa (xaritadan tanlagan bo‘lsa)
        elif lat and lng:
            pickup_points = PickupPoint.objects.annotate(
                distance=(
                    (F("latitude") - float(lat)) ** 2
                    + (F("longitude") - float(lng)) ** 2
                )
            ).order_by("distance")[
                :5
            ]  #  Eng yaqin 5 ta punktni qaytaradigan logika

            pickup_points = filter_by_language(
                pickup_points, lang, {"address": ("address_uz", "address_ru")}
            )
            return Response(
                PickupPointSerializer(pickup_points, many=True).data,
                status=status.HTTP_200_OK,
            )

        #  Agar hech qanday filter berilmasa, xatolik qaytaramiz
        return Response(
            {"error": "Viloyat, tuman yoki koordinata (lat/lng) talab qilinadi"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserDeliveryPriceAPI(APIView):
    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        currency = request.query_params.get("currency", "usd")
        rates = get_conversion_rates()

        region_id = request.query_params.get("region_id")
        lat = request.query_params.get("lat")
        lng = request.query_params.get("lng")

        if region_id:
            delivery_price = DeliveryPrice.objects.filter(region_id=region_id).first()
        elif lat and lng:
            region = (
                Region.objects.annotate(
                    distance=(F("latitude") - float(lat)) ** 2
                    + (F("longitude") - float(lng)) ** 2
                )
                .order_by("distance")
                .first()
            )
            delivery_price = DeliveryPrice.objects.filter(region=region).first()
        else:
            return Response(
                {"error": "Viloyat ID yoki koordinata kerak"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not delivery_price:
            return Response(
                {"error": "Yetkazib berish narxi topilmadi"},
                status=status.HTTP_404_NOT_FOUND,
            )

        original_price = delivery_price.price
        converted_price = original_price

        try:
            converted_price = convert_price(original_price, currency, rates)
        except Exception as e:
            logger.error(f"❌ Konvertatsiya xatosi: {str(e)}")
            converted_price = original_price

        return Response(
            {
                "region": RegionSerializer(
                    delivery_price.region, context={"lang": lang}
                ).data,
                "original_price": str(original_price),
                "converted_price": str(converted_price),
                "currency": currency,
                "delivery_time": delivery_price.delivery_time,
            },
            status=status.HTTP_200_OK,
        )


class UserPickupOrderAPI(APIView):
    def post(self, request):
        """Foydalanuvchi olib ketish buyurtmasi qiladi"""
        data = request.data
        products_data = data.pop("products", [])

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()

            for product_data in products_data:
                product_id = product_data["id"]
                quantity = product_data.get("quantity", 1)

                try:
                    product = Product.objects.get(id=product_id)
                    OrderProduct.objects.create(
                        order=order, product=product, quantity=quantity
                    )
                except Product.DoesNotExist:
                    return Response(
                        {"error": f"Mahsulot ID {product_id} topilmadi"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {"message": "Order placed", "id": order.id},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeliveryOrderAPI(APIView):
    def post(self, request):
        """Foydalanuvchi yetkazib berish tanlasa"""
        data = request.data
        products_data = data.pop("products", [])

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()

            for product_data in products_data:
                product_id = product_data["id"]
                quantity = product_data.get("quantity", 1)

                try:
                    product = Product.objects.get(id=product_id)
                    OrderProduct.objects.create(
                        order=order, product=product, quantity=quantity
                    )
                except Product.DoesNotExist:
                    return Response(
                        {"error": f"Mahsulot ID {product_id} topilmadi"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {"message": "Order placed", "id": order.id},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCommentsAPI(APIView):
    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        currency = request.query_params.get("currency", "usd")
        rates = get_conversion_rates()

        orders = Order.objects.exclude(comment__isnull=True).exclude(comment__exact="")

        comments = [
            {
                "user": order.name,
                "comment": order.comment,
                "image": order.image.url if order.image else None,
                "video": order.video.url if order.video else None,
                "products": ProductSerializer(
                    apply_currency_conversion(
                        filter_by_language(
                            order.products.all(),
                            lang,
                            {"name": ("name_uz", "name_ru")},
                        ),
                        currency,
                        rates,
                    ),
                    many=True,
                ).data,
            }
            for order in orders
        ]

        return Response(comments, status=status.HTTP_200_OK)


class UserRegionDetectAPI(APIView):
    """Foydalanuvchi joylashuviga yaqin viloyatni aniqlab olMI"""

    def get(self, request):
        lat = request.query_params.get("lat")
        lng = request.query_params.get("lng")

        if not lat or not lng:
            return Response(
                {"error": "Latitude va Longitude talab qilinadi iltimos kiriting "},
                status=status.HTTP_400_BAD_REQUEST,
            )

        #  Eng yaqin viloyatni topamiz
        region = (
            Region.objects.annotate(
                distance=(
                    (F("latitude") - float(lat)) ** 2
                    + (F("longitude") - float(lng)) ** 2
                )
            )
            .order_by("distance")
            .first()
        )

        if not region:
            return Response(
                {"error": "Hudud topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(RegionSerializer(region).data, status=status.HTTP_200_OK)
