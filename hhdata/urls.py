from django.urls import path

from . import views

app_name = 'hhdata'
urlpatterns = [
    path('', views.get_name, name='hhdata'),
]