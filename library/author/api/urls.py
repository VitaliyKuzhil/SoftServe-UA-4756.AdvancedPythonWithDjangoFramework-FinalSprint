from django.urls import path
from .views import AuthorListApiView

urlpatterns = [
    path('author/', AuthorListApiView.as_view()),
    path('author/<int:id>/', AuthorListApiView.as_view()),
]