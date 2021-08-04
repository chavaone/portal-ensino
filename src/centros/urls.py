from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import todos_os_centros, datos_centro, listas_usuario


urlpatterns = [
    path('centros/', TemplateView.as_view(template_name='appcentros.html'), name='appcentros'),
    path('centros/api', todos_os_centros, name='apicentros'),
    path('centros/api/centro/<int:codigo_req>', datos_centro, name='datoscentro'),
    path('centros/api/listas/<int:pk_lista>', listas_usuario, name='listas'),
    path('centros/api/listas/', listas_usuario, name='listas'),
]
