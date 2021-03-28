from django.db import models
#from datetime import datetime  
from django.utils import timezone
from socios.models import Familia

# Create your models here.

class PlanDePago(models.Model):
    crm_id = models.CharField(max_length=30)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    creado = models.DateTimeField('creado',default=timezone.now())
    actualizado = models.DateTimeField('actualizado',default=timezone.now())
    cantidad_cuotas = models.IntegerField('cantidad_cuotas')
    vto_primera_cuota = models.DateField('vto_primera_cuota')
    importe_cuota = models.FloatField() 
class CuotaSocialFamilia(models.Model):
    vencimiento = models.DateField('vencimiento')
    importe_cuota = models.FloatField()
    creado = models.DateTimeField('creado',default=timezone.now())
    actualizado = models.DateTimeField('actualizado',default=timezone.now())
    plan_de_pago = models.ForeignKey(PlanDePago, on_delete=models.CASCADE)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    pass

class CuotaPago(models.Model):
    cobrado = models.DateField('cobrado')
    creado = models.DateTimeField('creado',default=timezone.now())
    actualizado = models.DateTimeField('actualizado',default=timezone.now())
    aplica_cuota = models.ForeignKey(CuotaSocialFamilia, on_delete=models.CASCADE)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    pass
