from django.db import models

# Create your models here.

class Familia(models.Model):
    familia_crm_id = models.CharField(max_length=50)
    creado = models.DateTimeField('creado')
    actualizado = models.DateTimeField('actualizado')
    pass

class Socio(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField('fecha_nacimiento')
    creado = models.DateTimeField('creado')
    actualizado = models.DateTimeField('actualizado') 
    familia=models.ForeignKey(Familia, on_delete=models.CASCADE)
    pass



