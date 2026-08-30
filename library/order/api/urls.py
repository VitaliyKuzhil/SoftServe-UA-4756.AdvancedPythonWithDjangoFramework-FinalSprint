from django.urls import path
from rest_framework import routers

from order.api.views import OrderViewSet

order_router = routers.SimpleRouter()

order_router.register('', OrderViewSet, basename='order')

urlpatterns = order_router.urls
