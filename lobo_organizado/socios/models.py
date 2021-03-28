from django.db import models
from django.utils import timezone

# Create your models here.

class Familia(models.Model):
    familia_crm_id = models.CharField(max_length=50)
    creado = models.DateTimeField('creado',default=timezone.now())
    actualizado = models.DateTimeField('actualizado',default=timezone.now())
    pass

class Socio(models.Model):

    CATEGORIAS_CHOISES = [
        ( 0,"inactivo"),
        ( 1,"beneficiario"),
        ( 2,"dirigente"),
        ( 3,"resp.beneficiario"),
        ( 4,"colaborador")
        ]
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField('fecha_nacimiento')
    creado = models.DateTimeField('creado',default=timezone.now())
    actualizado = models.DateTimeField('actualizado',default=timezone.now())
    familia=models.ForeignKey(Familia, on_delete=models.CASCADE)
    categoria=models.IntegerField(default=0, choices=CATEGORIAS_CHOISES)
    pass


    

