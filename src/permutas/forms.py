from django import forms
from .models import PreferenciasPermutas, SITUACIONS
from centros.models import Centro, ListaCentros
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import InlineRadios

class FormPreferenciasPermutas(forms.ModelForm):
    situacion =  forms.ChoiceField(choices=SITUACIONS, widget=forms.RadioSelect(), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', False)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("""
            <h5>Centros e situación administrativa</h5>
            <p>Tes que completar todos os campos desta sección para activar a busca de permutas.</p>
            """),
            Row(
                Column('centro_actual'),
                Column('lista_peticiones'),
            ),
            'especialidad',
            InlineRadios('situacion'),
            FloatingField('info_centro'),
            HTML("""
            <h5>Información de Contacto</h5>
            <p>Só se amosará a aqueles usuarios cos que teñas unha posible permuta.</p>
            """),
            Row(
                Column(FloatingField('tlf_contacto')),
                Column(FloatingField('email_contacto')),
            ),
            FloatingField('otro_contacto'),
            HTML("""
            <h5>Activar</h5>
            <p>Tes que ter completados todos os campos da sección "Centros e situación administrativa" para poder activalo.</p>
            """),
            'activar_permutas',
            Submit('submit', 'Gardar')
        )

        if user:
            qs = ListaCentros.objects.filter(usuario=user)
        else:
            qs = ListaCentros.objects.none()
        self.fields['lista_peticiones'] = forms.ModelChoiceField(queryset=qs, required=False)

    class Meta:
        model = PreferenciasPermutas
        fields = ['activar_permutas',
                  'centro_actual',
                  'lista_peticiones',
                  'especialidad',
                  'situacion',
                  'info_centro',
                  'tlf_contacto',
                  'email_contacto',
                  'otro_contacto',
                  'publicar',
                  'texto_publico'
                  ]
        widgets = {
            'email_contacto': forms.EmailInput(),
            'otro_contacto': forms.Textarea(attrs={"rows":5}),
            'info_centro': forms.Textarea(attrs={"rows":5})
        }
        labels = {
            'tlf_contacto': "Teléfono",
            "email_contacto": "Email",
            "otro_contacto": "Máis información de contacto",
            "info_centro": "Máis información sobre o centro"
        }
