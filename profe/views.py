# profes/views.py
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import FormCreacionProfe

# Create your views here.

class SignUp(CreateView):
    form_class = FormCreacionProfe
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
