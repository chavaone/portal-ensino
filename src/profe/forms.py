# profes/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Profe
from django.utils.translation import ugettext_lazy as _

class FormCreacionProfe(UserCreationForm):

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@edu.xunta.es" not in data and "@edu.xunta.gal" not in data:
            raise forms.ValidationError(_("Email is not a Xunta de Galicia corporative email."))
        return data

    class Meta(UserCreationForm):
        model = Profe
        fields = ('email',)
        help_texts = {
            'email': _('Your email must be your corporative Xunta de Galicia one (usuario@edu.xunta.es, for example).'),
        }


class FormAutenticacionProfe(AuthenticationForm):
    def confirm_login_allowed(self, user):
        print("user -> " + user.email)
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive. You should check your email to activate it."),
                code='inactive',
            )

class FormDatosProfe(forms.ModelForm):

    class Meta:
        model = Profe
        fields = ('first_name',
                  'last_name',
                  )

class FormEliminarProfe (forms.Form):
    password = forms.CharField(label='Contrasinal', max_length=100, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user', None)
         super(FormEliminarProfe, self).__init__(*args, **kwargs)

    def clean_password (self):
        password = self.cleaned_data['password']

        if not self.user.check_password(password):
            raise forms.ValidationError(
                _('Password non valid'),
                code='incorrectpassword')

        return password
