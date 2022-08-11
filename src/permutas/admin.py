from django.contrib import admin
from .models import Permuta, PreferenciasPermutas

@admin.register(Permuta)
class PermutaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'profe_1', 'profe_2', 'permuta_ant', 'permuta_seg')


@admin.register(PreferenciasPermutas)
class PreferenciasPermutasAdmin(admin.ModelAdmin):
    pass
