from django.urls import path

from . import views

app_name = 'reservation'
urlpatterns = [
    path('', views.index, name='index')
]