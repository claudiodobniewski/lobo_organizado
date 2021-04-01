from django.db import models
from socios.models import Familia
from datetime import date

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
    
    def __str__(self):
        return  "Concepto: {} | Familia:{} | Vto:{}".format(self.plan_de_pago,self.familia, self.vencimiento)

# Pagos de una familia a cuenta de un plan
class CuotaPago(models.Model):
    importe = models.FloatField('cobrado',default=0.0)
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    fecha_cobro = models.DateField('fecha_cobro',default=date.today)
    aplica_cuota = models.ForeignKey(CuotaSocialFamilia, on_delete=models.CASCADE)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    
    def __str__(self):
        return  "Concepto: {} | Familia:{} | Vto:{}".format(self.aplica_cuota,self.familia, self.importe)
