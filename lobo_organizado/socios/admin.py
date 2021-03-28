from django.contrib import admin

from .models import Familia
from .models import Socio


class SociosInline(admin.StackedInline):
    model = Socio
    extra = 1
class FamiliaAdmin(admin.ModelAdmin):
    fields = ['familia_crm_id']
    list_display = ['familia_crm_id']
    inlines = [SociosInline]

class SocioAdmin(admin.ModelAdmin):
    fields = ['familia','nombres','apellidos','categoria','dni','fecha_nacimiento']
    list_display = ['familia','apellidos', 'nombres','categoria']

admin.site.register(Familia,FamiliaAdmin)
admin.site.register(Socio,SocioAdmin)