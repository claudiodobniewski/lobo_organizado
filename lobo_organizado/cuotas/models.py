from django.db import models

# Create your models here.

class CuotaFamiliaAnual(models.Model):
    vencimiento = models.DateTimeField('vencimiento')
    importe = models.FloatField()
    creado = models.DateTimeField('creado')
    actualizado = models.DateTimeField('actualizado')
    pass
