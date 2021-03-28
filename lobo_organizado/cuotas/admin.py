from django.contrib import admin

# Register your models here.
from .models import CuotaSocialFamilia
from .models import PlanDePago
from .models import CuotaPago





class PlanDePagoAdmin(admin.ModelAdmin):
    fields = ['crm_id','nombre','descripcion','cantidad_cuotas','vto_primera_cuota','importe_cuota','creado', 'actualizado']

class CuotaSocialFamiliaAdmin(admin.ModelAdmin):
    fields = ['familia','plan_de_pago','vencimiento','importe_cuota','creado', 'actualizado']
class CuotaPagonAdmin(admin.ModelAdmin):
    fields = ['cobrado','aplica_cuota','familia','creado', 'actualizado']

admin.site.register(PlanDePago,PlanDePagoAdmin)
admin.site.register(CuotaSocialFamilia,CuotaSocialFamiliaAdmin)
admin.site.register(CuotaPago,CuotaPagonAdmin)