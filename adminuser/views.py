from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order_and_zayavka.models.order import Order
from order_and_zayavka.Serializers.order import OrderSerializer


class AdminLoginAPI(APIView):
    """Admin uchun Login API qismi"""

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(
            {
                "error": "Noto‘g‘ri login yoki parol kiritdingiz iltimos qaytadan urinib kpring"
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class AdminLogoutAPI(APIView):
    """Admin uchun Logout API qismi"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({"message": "Admin logout bo‘ldi"}, status=status.HTTP_200_OK)


class AdminUserListAPI(APIView):
    """Admin uchun buyurtmachilar ro‘yxati"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyers = Order.objects.values("id", "name", "phone").distinct()
        return Response(buyers, status=status.HTTP_200_OK)


class AdminUserDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """Admin uchun buyurtmachi tafsilotlari"""

    # The lines `authentication_classes = [TokenAuthentication]` and `permission_classes =
    # [IsAuthenticated]` are used in Django REST framework to specify the authentication and permission
    # classes that should be applied to a particular view.
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        orders = Order.objects.filter(id=id)
        if not orders.exists():
            return Response(
                {"error": "Buyurtmachi topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        order_serializer = OrderSerializer(orders, many=True)

        data = {
            "user": {
                "name": orders.first().name,
                "phone": orders.first().phone,
            },
            "orders": order_serializer.data,  # Buyurtmalar tarixi korish uchun
        }

        return Response(data, status=status.HTTP_200_OK)


class AdminOrderFilterAPI(APIView):
    """Admin uchun buyurtmalarni status bo‘yicha filterlash qismi"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get("status")  # `status` parametri olamiz

        if status_filter:
            orders = Order.objects.filter(status=status_filter)
        else:
            orders = Order.objects.all()

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)
