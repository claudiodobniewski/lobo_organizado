from django.contrib import admin

from .models import Familia, Socio, Observaciones


class SociosInline(admin.StackedInline):
    model = Socio
    extra = 0

class ObservacionesInline(admin.StackedInline):
    model = Observaciones
    extra = 1
class FamiliaAdmin(admin.ModelAdmin):
    fields = ['familia_crm_id']
    list_display = ['familia_crm_id']
    #inlines = [SociosInline]
    inlines = [SociosInline,ObservacionesInline]

class SocioAdmin(admin.ModelAdmin):
    fields = ['familia','nombres','apellidos','categoria','dni','fecha_nacimiento']
    list_display = ['familia','apellidos', 'nombres','categoria']

class ObservacionesAdmin(admin.ModelAdmin):
    fields = ['descripcion','actualizado']
    list_display = ['descripcion','actualizado']

admin.site.register(Familia,FamiliaAdmin)
admin.site.register(Socio,SocioAdmin)
#admin.site.register(Observaciones,ObservacionesInline)