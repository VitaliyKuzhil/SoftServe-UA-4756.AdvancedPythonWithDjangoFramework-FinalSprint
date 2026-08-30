from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from authentication.models import CustomUser
from order.models import Order
from .serializers import UserSerializer
from order.api.serializers import OrderSerializer



class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = [AllowAny]


    @action(detail=True, methods=['get'], url_path=r'order')
    def get_orders(self, request, pk=None):
        user = self.get_object() 
        orders = Order.objects.filter(user_id=user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['get'], url_path=r'order/(?P<order_id>\d+)')
    def get_specific_order(self, request, pk=None, order_id=None):
        order = get_object_or_404(Order, id=order_id, user_id=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)



class UserOrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        order_id = self.kwargs.get('pk')
        return get_object_or_404(Order, id=order_id, user_id=user_id)