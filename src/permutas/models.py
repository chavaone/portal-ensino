from django.db import models
from profe.models import Profe
from centros.models import ListaCentros, Centro
from .especialidades import ESPECIALIDADES
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

SITUACIONS = (
    ('D', 'Con destino definitivo'),
    ('P', 'Docente en expectativa de destino'),
    ('I', 'Interino')
)

class PreferenciasPermutas(models.Model):

    usuario = models.ForeignKey(
        Profe,
        on_delete=models.CASCADE
    )

    activar_permutas = models.BooleanField(default=False)
    centro_actual = models.ForeignKey(
        Centro,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    lista_peticiones = models.ForeignKey(
        ListaCentros,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    especialidad = models.IntegerField(
        choices = ESPECIALIDADES,
        blank=True,
        null=True
    )
    situacion = models.CharField(
        max_length=1,
        choices=SITUACIONS,
        blank=True,
        null=True
    )
    info_centro =  models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    #INFO Contacto
    telefono_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    tlf_contacto = models.CharField(
        validators=[telefono_regex], # validators should be a list
        max_length=17,
        blank=True,
        null=True
    )
    email_contacto = models.EmailField(
        blank=True,
        null=True
    )
    otro_contacto =  models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    #Publico
    publicar = models.BooleanField(default=False)
    texto_publico = models.CharField(
        max_length=500,
        blank=True)

    def __str__(self):
        return self.usuario.email


class Permuta(models.Model):
    dataehora = models.DateTimeField(
        auto_now_add=True
    )
    profe_1 = models.ForeignKey(
        PreferenciasPermutas,
        related_name='pro_1',
        on_delete=models.CASCADE
    )
    profe_2 = models.ForeignKey(
        PreferenciasPermutas,
        related_name='pro_2',
        on_delete=models.CASCADE
    )
    permuta_ant = models.ForeignKey(
        "self",
        related_name='per_ant',
        on_delete = models.CASCADE,
        null=True,
    )
    permuta_seg = models.ForeignKey(
        "self",
        related_name='per_seg',
        on_delete = models.CASCADE,
        null=True,
    )
