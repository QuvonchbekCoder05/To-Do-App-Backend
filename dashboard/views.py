from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import count_unique_visitors
from dashboard.models import SiteVisit
from order_and_zayavka.models.order import Order


class AdminDashboardAPI(APIView):
    """Admin uchun Dashboard ma’lumotlari"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count_unique_visitors(request)  # Yangi tashrifni hisoblaymiz

        total_orders = Order.objects.count()
        finished_orders = Order.objects.filter(status="finished").count()
        rejected_orders = Order.objects.filter(status="rejected").count()
        site_visits = SiteVisit.objects.count()  # Umumiy tashriflar

        data = {
            "total_orders": total_orders,
            "finished_orders": finished_orders,
            "rejected_orders": rejected_orders,
            "site_visits": site_visits,  # Sayt tashriflari
        }

        return Response(data)
