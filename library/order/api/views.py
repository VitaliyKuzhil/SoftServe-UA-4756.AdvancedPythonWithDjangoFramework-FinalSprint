from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from order.models import Order
from .serializers import OrderSerializer



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [AllowAny]
