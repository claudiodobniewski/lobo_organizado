from django.db import models


# Create your models here.

  
class Familia(models.Model):
    
    familia_crm_id = models.CharField(max_length=50)
    crm_id = models.IntegerField(default=0) # unique=True
    direccion_calle = models.CharField(max_length=50,blank=True)
    direccion_numero = models.CharField(max_length=50,blank=True)
    direccion_depto = models.CharField(max_length=50,blank=True)
    direccion_localidad = models.CharField(max_length=50,blank=True)
    direccion_provincia = models.CharField(max_length=50,blank=True)
    contacto = models.CharField(max_length=200,blank=True)
    
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    
    def __str__(self):
        return  self.familia_crm_id

class Socio(models.Model):

    CATEGORIAS_CHOISES = [
        ( 0,"inactivo"),
        ( 1,"beneficiario"),
        ( 2,"dirigente"),
        ( 3,"recurso adulto"),
        ( 4,"resp.beneficiario"),
        ( 5,"colaborador")
        ]

    RAMAS_CHOISES = [
        ( 0,"ninguna"),
        ( 1,"manada"),
        ( 2,"unidad scout"),
        ( 3,"caminantes"),
        ( 4,"rovers")
        ]

    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    dni = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField('fecha_nacimiento')
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    familia=models.ForeignKey(Familia, on_delete=models.CASCADE)
    categoria=models.IntegerField(default=0, choices=CATEGORIAS_CHOISES)
    rama=models.IntegerField(default=0, choices=RAMAS_CHOISES)

    def __str__(self):
        return  "{}, {}".format(self.apellidos,self.nombres)

 
class Observaciones(models.Model):
    
    detalle = models.CharField(max_length=400)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE,blank=True, null=True)
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    
    def __str__(self):
        return  "{}, {}".format(self.familia.familia_crm_id,self.pk)
