# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('activePlayers/', views.ActivePlayers.as_view()), 
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]