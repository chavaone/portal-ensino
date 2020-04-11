from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('centros/', TemplateView.as_view(template_name='appcentros.html'), name='appcentros'),
]
