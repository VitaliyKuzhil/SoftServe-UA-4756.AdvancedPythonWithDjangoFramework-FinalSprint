from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_of_orders, name='list_of_orders'),
    path('create/', views.create_an_order, name='create_an_order'),
    path('<int:user_id>/', views.user_orders, name='user_orders'),
    path('order_status/<int:order_id>/', views.status_an_order, name='status_an_order')
]