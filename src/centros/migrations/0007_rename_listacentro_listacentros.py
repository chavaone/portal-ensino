# Generated by Django 3.2.5 on 2021-08-01 21:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('centros', '0006_listacentro'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ListaCentro',
            new_name='ListaCentros',
        ),
    ]
