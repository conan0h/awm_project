from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_nearby_wikipedia, name='get_nearby_wikipedia'),
    path('get_location/', views.get_nearby_wikipedia, name='get_nearby_wikipedia'),
]
