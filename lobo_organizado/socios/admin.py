from django.contrib import admin

from .models import Familia
from .models import Socio


class FamiliaAdmin(admin.ModelAdmin):
    fields = ['familia_crm_id','creado', 'actualizado']

class SocioAdmin(admin.ModelAdmin):
    fields = ['familia','nombres','apellidos','categoria','dni','fecha_nacimiento','creado', 'actualizado']

admin.site.register(Familia,FamiliaAdmin)
admin.site.register(Socio,SocioAdmin)