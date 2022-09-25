from django.urls import path

from . import views

app_name = 'portraits'
urlpatterns = [
    path('', views.index, name='index'),
]
