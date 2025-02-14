from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import translate_and_store
from products.models.brand import Brand
from products.serializers.brand_serializer import BrandSerializer


class BrandAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            try:
                brand = Brand.objects.get(id=id)
                serializer = BrandSerializer(brand)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Brand.DoesNotExist:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )

        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            brand = serializer.save()
            translate_and_store(
                brand, [("name_uz", "name_ru")]
            )  # Brend nomi tarjima qilinadi agar bosh nbolas
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            brand = Brand.objects.get(id=id)
            serializer = BrandSerializer(brand, data=request.data, partial=True)
            if serializer.is_valid():
                brand = serializer.save()
                translate_and_store(
                    brand, [("name_uz", "name_ru")]
                )  #  Brend nomi tarjima qilinadi agar bosh bolsa uz maydoni
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Brand.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            brand = Brand.objects.get(id=id)
            brand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Brand.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
