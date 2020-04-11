from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

class Concello(models.Model):
    PROVINCIAS = [
        ('AC', _('A Coruña')),
        ('LU', _('Lugo')),
        ('OU', _('Ourense')),
        ('PO', _('Pontevedra')),
    ]
    nome = models.CharField(max_length=50,)
    provincia = models.CharField(
        max_length=2,
        choices=PROVINCIAS
    )

    def __str__(self):
        return self.nome

class Ensinanza (models.Model):
    TIPO_ENSINANZAS = [
        ('INF', _('Educación Infantil')),
        ('PRI', _('Educación Primaria')),
        ('ESO', _('Educación Secundaria Obrigatoria')),
        ('BAC', _('Bacharelato')),
        ('EBI', _('Educacións Básicas Iniciais')),
        ('ESA', _('Educación Secundaria para Adultos')),
        ('BACA', _('Bacharelato de Adultos')),
        ('ESP', _('Educación Especial')),
        ('FPB', _('Formación Profesional')),
        ('MUS', _('Música')),
        ('ARDE', _('Arte e Deseño')),
        ('IDI', _('Idiomas')),
        ('DAN', _('Danza')),
        ('ARDR', _('Arte Dramático'))
    ]
    TIPO_GRADO = [
        ('B', _('Básico')),
        ('M', _('Medio')),
        ('S', _('Superior'))
    ]
    tipo = models.CharField(
        max_length=4,
        choices=TIPO_ENSINANZAS
    )
    grado = models.CharField(
        max_length=1,
        choices=TIPO_GRADO,
        blank=True,
        null=True
    )
    nome = models.CharField(max_length=75,)

    def __str__(self):
        return self.tipo + " - " + self.nome

class Servizo (models.Model):
    nome = models.CharField(max_length=75,)

    def __str__(self):
        return self.nome

class Centro(models.Model):
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=50,)
    coorlat = models.DecimalField(max_digits=9, decimal_places=6)
    coorlon = models.DecimalField(max_digits=9, decimal_places=6)
    enderezo = models.CharField(max_length=100,)
    cp = models.IntegerField()
    concello = models.ForeignKey(
        Concello,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
        )
    web = models.URLField(blank=True, null=True)
    telefono_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    telefono = models.CharField(
        validators=[telefono_regex], # validators should be a list
        max_length=17,
        blank=True)
    email = models.EmailField(blank=True, null=True)
    ensinanzas = models.ManyToManyField(Ensinanza)
    servizos = models.ManyToManyField(Servizo)

    def __str__(self):
        return self.nome

class Xornada(models.Model):
    TIPO_XORNADA = [
        ('PA', _('Partida')),
        ('CO', _('Continua')),
        ('MI', _('Mixta'))
    ]
    TIPO_NIVEL = [
        ('IN', _('Infantil')),
        ('PR', _('Primaria')),
    ]
    centro = models.ForeignKey('Centro', on_delete=models.CASCADE)
    nivel = models.CharField(
        max_length=2,
        choices=TIPO_NIVEL,
    )
    tipo_xornada = models.CharField(
        max_length=2,
        choices=TIPO_XORNADA,
    )
