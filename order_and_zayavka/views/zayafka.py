# views/zayafka.py
from order_and_zayavka.models.Zayafka import Zayafka
from order_and_zayavka.Serializers.zayafka import ZayafkaSerializer
from order_and_zayavka.views.core import APIView, Response, status


# ADMIN ZAYAVKA API qsimi
class AdminZayafkaAPI(APIView):
    def get(self, request):
        zayavkalar = Zayafka.objects.all()
        serializer = ZayafkaSerializer(zayavkalar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
