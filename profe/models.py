from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


from django.utils.translation import ugettext_lazy as _


CORPOS = [
    ("PES",  "PROFESORES DE ENSEÑANZA SECUNDARIA"),
    ("PTFP", "PROFESORES TÉCNICOS DE FORMACIÓN PROFESIONAL"),
    ("PEOI", "PROFESORES DE ESCUELAS OFICIALES DE IDIOMAS"),
    ("PMAE", "PROFESORES DE MÚSICA Y ARTES ESCÉNICAS"),
    ("PAPD", "PROFESORES DE ARTES PLÁSTICAS Y DISEÑO"),
    ("MA",   "MAESTROS"),
]

class Especialidade (models.Model):
    codigo = models.IntegerField(unique=True)
    corpo = models.CharField(max_length=4, choices=CORPOS)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class ProfeManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Profe(AbstractUser):
    """ """
    #Modify username and email fields to use email to login
    username = None
    email = models.EmailField(_('email address'), unique=True)

    #Set email as login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = ProfeManager()

    #New fields
    #first_name, last_name
    especialidade = models.ForeignKey(
            Especialidade,
            blank=True,
            null=True,
            on_delete=models.SET_NULL,
    )
