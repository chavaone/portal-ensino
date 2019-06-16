# users/urls.py
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from .forms import FormAutenticacionProfe
from django.views.generic import TemplateView

urlpatterns = [
    path('inicio-sesion/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=FormAutenticacionProfe, ), name='login'),
    path('pechar-sesion/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('rexistro/', views.signup, name='rexistro'),
    path('conta/cambiar-contrasinal/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('conta/cambiar-contrasinal/feito', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('conta/reiniciar-contrasinal/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('conta/reiniciar-contrasinal/feito/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    re_path(r'^conta/reiniciar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('conta/reiniciar/feito/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    re_path(r'^activar-conta/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('conta/preferencias/', views.ModificarDatosProfe.as_view(), name='edit_profe_data'),
    path('conta/eliminar/', views.eliminar_profe, name='delete_profe'),
    path('conta/eliminar/feito/', TemplateView.as_view(template_name='profe_done_delete.html'), name='delete_profe_done'),
]
