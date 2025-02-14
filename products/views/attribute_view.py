from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import translate_and_store
from products.models.attribute import Attribute
from products.serializers.attribute_serializer import AttributeSerializer


class AttributeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        attributes = Attribute.objects.all()
        serializer = AttributeSerializer(attributes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            attribute = serializer.save()
            translate_and_store(
                attribute, [("key_uz", "key_ru"), ("value_uz", "value_ru")]
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            attribute = Attribute.objects.get(pk=pk)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AttributeSerializer(attribute, data=request.data)
        if serializer.is_valid():
            serializer.save()
            translate_and_store(
                serializer.instance, [("key_uz", "key_ru"), ("value_uz", "value_ru")]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            attribute = Attribute.objects.get(pk=pk)
        except Attribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        attribute.delete()
        return Response(status=status.HTTP_200_OK)
