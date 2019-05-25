from django.urls import path
from . import views

urlpatterns = [
    path('print/', views.print, name='print'),
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),
]
