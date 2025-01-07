from rest_framework import viewsets
from store.models import Order
from store.serializers.order_serializer import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
