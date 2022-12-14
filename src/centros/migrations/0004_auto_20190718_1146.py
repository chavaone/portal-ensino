# Generated by Django 2.2 on 2019-07-18 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centros', '0003_auto_20190717_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='ensinanza',
            name='grado',
            field=models.CharField(blank=True, choices=[('B', 'Básico'), ('M', 'Medio'), ('S', 'Superior')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='ensinanza',
            name='tipo',
            field=models.CharField(choices=[('INF', 'Educación Infantil'), ('PRI', 'Educación Primaria'), ('ESO', 'Educación Secundaria Obrigatoria'), ('BAC', 'Bacharelato'), ('EBI', 'Educacións Básicas Iniciais'), ('ESA', 'Educación Secundaria para Adultos'), ('BACA', 'Bacharelato de Adultos'), ('ESP', 'Educación Especial'), ('FPB', 'Formación Profesional'), ('MUS', 'Música'), ('ARDE', 'Arte e Deseño'), ('IDI', 'Idiomas'), ('DAN', 'Danza'), ('ARDR', 'Arte Dramático')], max_length=4),
        ),
    ]
