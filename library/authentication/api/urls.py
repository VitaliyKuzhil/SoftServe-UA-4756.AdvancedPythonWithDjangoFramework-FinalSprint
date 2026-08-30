from django.urls import path
from rest_framework import routers

from authentication.api.views import UserOrderDetailAPIView, UserViewSet

user_router = routers.SimpleRouter()

user_router.register('', UserViewSet, basename='user')


urlpatterns = [
    path('<int:user_id>/order/<int:pk>/', UserOrderDetailAPIView.as_view(), name='user-order-detail'),
]

urlpatterns = user_router.urls
