from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import filter_by_language, translate_and_store
from order_and_zayavka.models.delivery_method import (
    DeliveryPrice,
    District,
    PickupPoint,
    Region,
)
from order_and_zayavka.Serializers.delivery_method import (
    DeliveryPriceSerializer,
    DistrictSerializer,
    PickupPointSerializer,
    RegionSerializer,
)


#  ADMIN: Viloyat CRUD amallari
class AdminRegionAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        regions = filter_by_language(
            Region.objects.all(), lang, {"name": ("name_uz", "name_ru")}
        )
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            region = serializer.save()
            translate_and_store(region, [("name_uz", "name_ru")])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRegionDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            region = Region.objects.get(pk=pk)
            serializer = RegionSerializer(region)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Region.DoesNotExist:
            return Response(
                {"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            region = Region.objects.get(pk=pk)
            serializer = RegionSerializer(region, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Region.DoesNotExist:
            return Response(
                {"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            region = Region.objects.get(pk=pk)
            region.delete()
            return Response(
                {"message": "Region deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except Region.DoesNotExist:
            return Response(
                {"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND
            )


#  ADMIN: Tuman CRUD amallari
class AdminDistrictAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        districts = filter_by_language(
            District.objects.all(), lang, {"name": ("name_uz", "name_ru")}
        )
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DistrictSerializer(data=request.data)
        if serializer.is_valid():
            district = serializer.save()
            translate_and_store(district, [("name_uz", "name_ru")])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDistrictDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            district = District.objects.get(pk=pk)
            serializer = DistrictSerializer(district)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except District.DoesNotExist:
            return Response(
                {"error": "District not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            district = District.objects.get(pk=pk)
            serializer = DistrictSerializer(district, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except District.DoesNotExist:
            return Response(
                {"error": "District not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            district = District.objects.get(pk=pk)
            district.delete()
            return Response(
                {"message": "District deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except District.DoesNotExist:
            return Response(
                {"error": "District not found"}, status=status.HTTP_404_NOT_FOUND
            )


#  ADMIN: Olib ketish punktlari CRUD amallari
class AdminPickupPointAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lang = request.query_params.get("lang", "uz")
        points = filter_by_language(
            PickupPoint.objects.all(), lang, {"address": ("address_uz", "address_ru")}
        )
        serializer = PickupPointSerializer(points, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PickupPointSerializer(data=request.data)
        if serializer.is_valid():
            point = serializer.save()
            translate_and_store(point, [("address_uz", "address_ru")])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPickupPointDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            point = PickupPoint.objects.get(pk=pk)
            serializer = PickupPointSerializer(point)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PickupPoint.DoesNotExist:
            return Response(
                {"error": "Pickup Point not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            point = PickupPoint.objects.get(pk=pk)
            serializer = PickupPointSerializer(point, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PickupPoint.DoesNotExist:
            return Response(
                {"error": "Pickup Point not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            point = PickupPoint.objects.get(pk=pk)
            point.delete()
            return Response(
                {"message": "Pickup Point deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except PickupPoint.DoesNotExist:
            return Response(
                {"error": "Pickup Point not found"}, status=status.HTTP_404_NOT_FOUND
            )


#  ADMIN: Yetkazib berish narxlari CRUD amallri
class AdminDeliveryPriceAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        prices = DeliveryPrice.objects.all()
        serializer = DeliveryPriceSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DeliveryPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDeliveryPriceDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            price = DeliveryPrice.objects.get(pk=pk)
            serializer = DeliveryPriceSerializer(price)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DeliveryPrice.DoesNotExist:
            return Response(
                {"error": "Delivery Price not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            price = DeliveryPrice.objects.get(pk=pk)
            serializer = DeliveryPriceSerializer(price, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DeliveryPrice.DoesNotExist:
            return Response(
                {"error": "Delivery Price not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            price = DeliveryPrice.objects.get(pk=pk)
            price.delete()
            return Response(
                {"message": "Delivery Price deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except DeliveryPrice.DoesNotExist:
            return Response(
                {"error": "Delivery Price not found"}, status=status.HTTP_404_NOT_FOUND
            )
