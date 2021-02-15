from django.contrib import admin

from .models import Concello, Ensinanza,  Centro

@admin.register(Concello)
class ConcelloAdmin(admin.ModelAdmin):
    pass

@admin.register(Ensinanza)
class EnsinanzaAdmin(admin.ModelAdmin):
    pass

@admin.register(Centro)
class CentroAdmin(admin.ModelAdmin):
    pass
