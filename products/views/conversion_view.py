from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models.conversion import Conversion
from products.serializers.conversion_serializers import ConversionSerializer


class ConversionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversions = Conversion.objects.all()
        serializer = ConversionSerializer(conversions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ConversionSerializer(data=request.data)
        if serializer.is_valid():
            conversion = serializer.save()
            return Response(
                ConversionSerializer(conversion).data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, pk):
        try:
            conversion = Conversion.objects.get(pk=pk)
        except Conversion.DoesNotExist:
            return Response(
                {"error": "Conversion not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ConversionSerializer(conversion, data=request.data)
        if serializer.is_valid():
            conversion = serializer.save()
            return Response(
                ConversionSerializer(conversion).data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        try:
            deleted_count, _ = Conversion.objects.all().delete()
            return Response(
                {
                    "message": f"Barcha {deleted_count} ta Conversion elementlari o'chirildi."
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
