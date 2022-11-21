import datetime
from django.db import models
from socios.models import Familia
from datetime import date
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

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

    history = AuditlogHistoryField()

    class Meta:
        permissions = (
                       ( "planpago_crear","Agregar nuevo plan de pago"),
                       ( "planpago_editar","Editar plan de pago"),
                       ( "planpagos_borrar","Eliminar un plan de pago"),
                       ( "planpago_ver","Ver detalle de plan de pago" ),
                      )

    def __str__(self):
        return  "Pla{}:{}".format(self.pk,self.crm_id)
# cuotas del plan generadas a una familia
class CuotaSocialFamilia(models.Model):
    vencimiento = models.DateField('vencimiento')
    importe_cuota = models.FloatField()
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    plan_de_pago = models.ForeignKey(PlanDePago, on_delete=models.CASCADE)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    
    history = AuditlogHistoryField()
    class Meta:
        permissions = (
                       ( "cuota_crear","Agregar cuotas"),
                       ( "cuota_editar","Editar cuotas"),
                       ( "cuota_borrar","Eliminar cuotas"),
                       ( "cuota_ver","Ver detalle de cuotas" ),
                      )

    def __str__(self):
        return  "Cuo{}:{}:${}".format(self.pk,self.vencimiento,self.importe_cuota)

# Pagos de una familia a cuenta de un plan

class CuotaMedioDePago(models.Model):
    '''Medios de cobrod e cuotas'''
    medio_id = models.CharField(max_length=10,unique=True)
    descripcion = models.CharField(max_length=300)
    disponible = models.BooleanField(default=False)

    history = AuditlogHistoryField()
    
    def __str__(self):
        return  "{} - {}".format(self.medio_id,self.descripcion)

class CuotaPago(models.Model):

    importe = models.DecimalField('cobrado',default=0.0,max_digits=8,decimal_places=2,validators=[MinValueValidator(Decimal('1.0'))])
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    fecha_cobro = models.DateField('fecha_cobro',default=date.today,)
    aplica_pago_plan = models.ForeignKey(PlanDePago, on_delete=models.CASCADE)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    forma_de_pago = models.ForeignKey(CuotaMedioDePago,default=1, on_delete=models.CASCADE)
    comprobante = models.CharField(default="",blank=True,max_length=12)
    #hash = models.UUIDField(default=uuid.uuid4, editable=False)
    hash = models.CharField(default=uuid.uuid4,max_length=40 ,editable=True)

    history = AuditlogHistoryField()

    class Meta:
        permissions = (
                       ( "pago_cuota_crear","Agregar nuevos pagos de un plan a familia"),
                       ( "pago_cuota_editar","Editar pagos a un plan de la familia"),
                       ( "pago_cuota_borrar","Eliminar pagos de un plan a familia"),
                       ( "pago_cuota_ver","Ver detalle de pagos del plan a familia" ),
                      )
        
        #constraints = [
        #    models.CheckConstraint(check=models.Q(importe__gt=Decimal('0')), name='importe_gt_0'),
        #]
    def year_choices():
        return [(r,r) for r in range(datetime.date.today().year-2, datetime.date.today())]

    def current_year():
        return datetime.date.today().year
    
    def __str__(self):
        return  "Cob{}:{}:${}".format(self.pk,self.fecha_cobro,self.importe)
    





def cuotas_queryset(familia_id,deleted=False):
    '''return cuotas todas por familia '''
    return CuotaSocialFamilia.objects.filter( familia=familia_id,deleted=deleted )

### Filtra un QuerySet de cuotas por el plan_id, retorna subconjunto QuerySet
def cuotas_por_plan(cuotas, plan_id,deleted=False):
    '''return solo las cuotas del plan'''
    return cuotas.filter( plan_de_pago=plan_id,deleted=deleted )

### Filtra un QuerySet de cuotas por anteriores a la fecha de corte, retorna subconjunto QuerySet
def cuotas_vencidas(cuotas,fecha_de_corte):
    '''return cuotas con fecha anterior o igual a la fecha de corte'''
    # hoy datetime.date.today()
    return cuotas.exclude(vencimiento__gte=fecha_de_corte )

### Suma el importe de las cuotas, retorna un numero Decimal
def cuotas_suma(cuotas):
    '''suma importe total de las cuotas'''
    return sum([x.importe_cuota for x in cuotas ])

def pagos_percibidos_queryset(familia_id,deleted=False):
    '''return todas las cuotas de la familia'''
    return CuotaPago.objects.filter( familia=familia_id,deleted=deleted )

### Filtra un QuerySet de pagos por plan, retorna subconjunto QuerySet
# valor sumado de los pagos
def pagos_percibidos_plan(pagos, plan_id):
    '''return pagos correspondientes al plan'''
    if plan_id:
        return pagos.filter( aplica_pago_plan=plan_id )
    return pagos

### Suma el valor de los pagos, retorna un numero Decimal
def pagos_percibidos_suma(pagos):
    '''return suma total cobrada'''
    if not pagos:
        return 0
    return sum([x.importe for x in pagos ])



auditlog.register(PlanDePago,exclude_fields=['creado','actualizado'])
auditlog.register(CuotaSocialFamilia,exclude_fields=['creado','actualizado'])
auditlog.register(CuotaPago,exclude_fields=['creado','actualizado'])