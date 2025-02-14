from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import translate_and_store
from DesktopFPSGames.desktop_serializers import (
    DesktopAttributesSerializer,
    DesktopSerializer,
    DesktopTypeSerializer,
)
from DesktopFPSGames.models1.attributes import DesktopAttributes
from DesktopFPSGames.models1.desktop import Desktop
from DesktopFPSGames.models1.desktop_type import DesktopType


class DesktopAdminAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                desktop = Desktop.objects.get(pk=pk)
                return Response(
                    DesktopSerializer(desktop).data, status=status.HTTP_200_OK
                )
            except Desktop.DoesNotExist:
                return Response(
                    {"error": "Desktop topilmadi yoki yaratilmagan"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        desktops = Desktop.objects.all()
        return Response(
            DesktopSerializer(desktops, many=True).data, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = DesktopSerializer(data=request.data)
        if serializer.is_valid():
            attributes = request.data.get("attributes", [])
            desktop = serializer.save()
            desktop.attributes.set(attributes)
            translate_and_store(
                desktop, [("name_uz", "name_ru"), ("description_uz", "description_ru")]
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            desktop = Desktop.objects.get(pk=pk)
        except Desktop.DoesNotExist:
            return Response(
                {"error": "Desktop topilmadi yoki yaratilmadi "},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DesktopSerializer(desktop, data=request.data, partial=True)
        if serializer.is_valid():
            attributes = request.data.get("attributes", None)
            desktop = serializer.save()
            if attributes is not None:
                desktop.attributes.set(attributes)
            translate_and_store(
                desktop, [("name_uz", "name_ru"), ("description_uz", "description_ru")]
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            desktop = Desktop.objects.get(pk=pk)
            desktop.delete()
            return Response(
                {"message": "O‘chirildi"}, status=status.HTTP_204_NO_CONTENT
            )
        except Desktop.DoesNotExist:
            return Response(
                {"error": "Desktop topilmadi yoki yaratilmagan "},
                status=status.HTTP_404_NOT_FOUND,
            )


class DesktopTypeAdminAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            try:
                desktop_type = DesktopType.objects.get(pk=pk)
                return Response(DesktopTypeSerializer(desktop_type).data)
            except DesktopType.DoesNotExist:
                return Response(
                    {"error": "Desktop Type topilmadi yoki yaratilmadi"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            desktop_types = DesktopType.objects.all()
            return Response(DesktopTypeSerializer(desktop_types, many=True).data)

    def post(self, request):
        serializer = DesktopTypeSerializer(data=request.data)
        if serializer.is_valid():
            desktop_type = serializer.save()
            translate_and_store(desktop_type, [("name_uz", "name_ru")])  # 🔥 Tarjima
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            desktop_type = DesktopType.objects.get(pk=pk)
        except DesktopType.DoesNotExist:
            return Response(
                {"error": "Desktop Type topilmadi yoki yaratilmagan"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DesktopTypeSerializer(
            desktop_type, data=request.data, partial=True
        )
        if serializer.is_valid():
            desktop_type = serializer.save()
            translate_and_store(desktop_type, [("name_uz", "name_ru")])  # 🔥 Tarjima
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            desktop_type = DesktopType.objects.get(pk=pk)
            desktop_type.delete()
            return Response(
                {"message": "O‘chirildi"}, status=status.HTTP_204_NO_CONTENT
            )
        except DesktopType.DoesNotExist:
            return Response(
                {"error": "Desktop Type topilmadi yoki yaratilmagan"},
                status=status.HTTP_404_NOT_FOUND,
            )


class DesktopAttributesAdminAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            try:
                attribute = DesktopAttributes.objects.get(pk=pk)
                return Response(DesktopAttributesSerializer(attribute).data)
            except DesktopAttributes.DoesNotExist:
                return Response(
                    {"error": "Desktop Attribute topilmadi yoki yaratilmagan "},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            attributes = DesktopAttributes.objects.all()
            return Response(DesktopAttributesSerializer(attributes, many=True).data)

    def post(self, request):
        serializer = DesktopAttributesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            attribute = DesktopAttributes.objects.get(pk=pk)
            serializer = DesktopAttributesSerializer(
                attribute, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DesktopAttributes.DoesNotExist:
            return Response(
                {"error": "Desktop Attribute topilmadi yoki yaratilmagan "},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, pk):
        try:
            attribute = DesktopAttributes.objects.get(pk=pk)
            attribute.delete()
            return Response(
                {"message": "O‘chirildi"}, status=status.HTTP_204_NO_CONTENT
            )
        except DesktopAttributes.DoesNotExist:
            return Response(
                {"error": "Desktop Attribute topilmadi yoki yaratilmagan "},
                status=status.HTTP_404_NOT_FOUND,
            )
