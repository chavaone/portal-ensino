# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('inicio-sesion/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('pechar-sesion/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('cambiar-contrasinal/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('cambiar-contrasinal/feito', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('reiniciar-contrasinal/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('reiniciar-contrasinal/feito/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reiniciar/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reiniciar/feito/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('rexistro/', views.SignUp.as_view(), name='rexistro'),
]
