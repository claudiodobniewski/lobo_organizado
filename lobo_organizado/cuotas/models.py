import datetime
from django.db import models
from socios.models import Familia
from datetime import date
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

# template de plan de pagos para generar las cuotas del plan e identificarlas
class PlanDePago(models.Model):
    crm_id = models.CharField(max_length=30)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    cantidad_cuotas = models.IntegerField('cantidad_cuotas')
    vto_primera_cuota = models.DateField('vto_primera_cuota')
    importe_cuota = models.FloatField()
    eliminado = models.BooleanField(default=False)
    orden = models.IntegerField(null=True, default=0)
    plan_default = models.BooleanField(default=False)

    class Meta:
        permissions = (
                       ( "planpago_crear","Agregar nuevo plan de pago"),
                       ( "planpago_editar","Editar plan de pago"),
                       ( "planpagos_borrar","Eliminar un plan de pago"),
                       ( "planpago_ver","Ver detalle de plan de pago" ),
                      )

    def __str__(self):
        return  "{}".format(self.nombre)
# cuotas del plan generadas a una familia
class CuotaSocialFamilia(models.Model):
    vencimiento = models.DateField('vencimiento')
    importe_cuota = models.FloatField()
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    plan_de_pago = models.ForeignKey(PlanDePago, on_delete=models.CASCADE)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return  "#{} Plan: {} | Familia:{} | Vto:{} | ${}".format(self.pk,self.plan_de_pago,self.familia, self.vencimiento,self.importe_cuota)

# Pagos de una familia a cuenta de un plan
class CuotaPago(models.Model):
    importe = models.DecimalField('cobrado',default=0.0,max_digits=8,decimal_places=2,validators=[MinValueValidator(Decimal('1.0'))])
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    fecha_cobro = models.DateField('fecha_cobro',default=date.today,)
    #aplica_cuota = models.ForeignKey(CuotaSocialFamilia, on_delete=models.CASCADE)
    aplica_pago_plan = models.ForeignKey(PlanDePago, on_delete=models.CASCADE)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    class Meta:
        permissions = (
                       ( "plan_cuota_crear","Agregar nuevas cuotas de un plan a familia"),
                       ( "plan_cuota_editar","Editar cuotas de un plan a familia"),
                       ( "plan_cuota_borrar","Eliminar cuotas de un plan a familia"),
                       ( "plan_cuota_ver","Ver detalle de cuotas del plan a familia" ),
                      )
        
        #constraints = [
        #    models.CheckConstraint(check=models.Q(importe__gt=Decimal('0')), name='importe_gt_0'),
        #]
    def year_choices():
        return [(r,r) for r in range(datetime.date.today().year-2, datetime.date.today())]

    def current_year():
        return datetime.date.today().year
    
    def __str__(self):
        return  "Concepto: {} | Familia:{} | Vto:{}".format(self.aplica_pago_plan,self.familia, self.importe)


def cuotas_queryset(familia_id,deleted=False):
    return CuotaSocialFamilia.objects.filter( familia=familia_id,deleted=deleted )

### Filtra un QuerySet de cuotas por el plan_id, retorna subconjunto QuerySet
def cuotas_por_plan(cuotas, plan_id,deleted=False):
    return cuotas.filter( plan_de_pago=plan_id )

### Filtra un QuerySet de cuotas por anteriores a la fecha de corte, retorna subconjunto QuerySet
def cuotas_vencidas(cuotas,fecha_de_corte):
    # hoy datetime.date.today()
    return cuotas.exclude(vencimiento__gte=fecha_de_corte )

### Suma el importe de las cuotas, retorna un numero Decimal
def cuotas_suma(cuotas):
    return sum([x.importe_cuota for x in cuotas ])

def pagos_percibidos_queryset(familia_id,deleted=False):
    return CuotaPago.objects.filter( familia=familia_id,deleted=deleted )

### Filtra un QuerySet de pagos por plan, retorna subconjunto QuerySet
# valor sumado de los pagos
def pagos_percibidos_plan(pagos, plan_id):
    pagos.filter( plan_id=plan_id )

### Suma el valor de los pagos, retorna un numero Decimal
def pagos_percibidos_suma(pagos):
    if not pagos:
        return 0
    return sum([x.importe for x in pagos ])