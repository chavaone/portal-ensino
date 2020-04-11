from django.contrib import admin

from .models import Concello, Ensinanza, Servizo, Centro, Xornada

@admin.register(Concello)
class ConcelloAdmin(admin.ModelAdmin):
    pass

@admin.register(Ensinanza)
class EnsinanzaAdmin(admin.ModelAdmin):
    pass

@admin.register(Servizo)
class ServizoAdmin(admin.ModelAdmin):
    pass

@admin.register(Centro)
class CentroAdmin(admin.ModelAdmin):
    pass

@admin.register(Xornada)
class XornadaAdmin(admin.ModelAdmin):
    pass
