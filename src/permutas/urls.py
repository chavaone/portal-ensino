#permutas/urls.py
from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('conta/permutas/', login_required(views.ModificarPreferenciasPermutas.as_view()), name='edit_profe_permutas'),
    path('permutas/calculo/<codigo>', views.calcular_permutas, name="calculo_permutas"),
    path('permutas/', views.ver_permutas, name="ver_permutas")
]
