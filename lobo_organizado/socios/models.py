from django.db import models
#from django.utils import timezone
from datetime import datetime 

# Create your models here.

class Familia(models.Model):
    
    familia_crm_id = models.CharField(max_length=50)
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    
    def __str__(self):
        return  self.familia_crm_id

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
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    familia=models.ForeignKey(Familia, on_delete=models.CASCADE)
    categoria=models.IntegerField(default=0, choices=CATEGORIAS_CHOISES)

    def __str__(self):
        return  "{}, {}".format(self.apellidos,self.nombres)


    

