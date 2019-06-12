# profes/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profe

class FormCreacionProfe(UserCreationForm):

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@edu.xunta.es" not in data and "@edu.xunta.gal" not in data:   # any check you need
            raise forms.ValidationError("EMAIL MAL") #TODO
        return data

    class Meta(UserCreationForm):
        model = Profe
        fields = ('email',)
