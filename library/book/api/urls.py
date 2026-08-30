from django.urls import path
from .views import BookListApiView

urlpatterns = [
    path('book/', BookListApiView.as_view()),
    path('book/<int:id>/', BookListApiView.as_view()),
]