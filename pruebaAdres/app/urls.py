from django.urls import path
from .views import cargar_archivo

urlpatterns = [
    path('', cargar_archivo, name='cargar_archivo'),
]