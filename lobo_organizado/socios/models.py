from django.db import models


# Create your models here.

  
class Familia(models.Model):
    
    familia_crm_id = models.CharField(max_length=50)
    crm_id = models.IntegerField(unique=True) # unique=True
    direccion_calle = models.CharField(max_length=50,blank=True)
    direccion_numero = models.CharField(max_length=50,blank=True)
    direccion_depto = models.CharField(max_length=50,blank=True)
    direccion_localidad = models.CharField(max_length=50,blank=True)
    direccion_provincia = models.CharField(max_length=50,blank=True)
    contacto = models.CharField(max_length=200,blank=True)
    eliminado = models.BooleanField(default=False)
    
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    
    class Meta:
        permissions = (
                       ( "familia_crear","Agregar nueva familia"),
                       ( "familia_editar","Editar familia"),
                       ( "familia_borrar","Eliminar familia"),
                       ( "familia_ver","Ver informacion de familia" ),
                      )

    def __str__(self):
        return  self.familia_crm_id

class Socio(models.Model):

    CATEGORIAS_CHOISES = [
        ( -1,"no_socio"),
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
    dni = models.CharField(max_length=15,unique=True)
    fecha_nacimiento = models.DateField('fecha_nacimiento',null=True)
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    familia=models.ForeignKey(Familia, on_delete=models.CASCADE)
    categoria=models.IntegerField(default=0, choices=CATEGORIAS_CHOISES)
    rama=models.IntegerField(default=0, choices=RAMAS_CHOISES)

    class Meta:
        permissions = (
                       ( "socio_crear","Agregar nuevo socio a una familia"),
                       ( "socio_editar","Editar socio"),
                       ( "socio_borrar","Eliminar socio"),
                       ( "socio_ver","Ver informacion de un socio" ),
                      )

    def __str__(self):
        return  "{}, {}".format(self.apellidos,self.nombres)

 
class Observaciones(models.Model):
    
    detalle = models.CharField(max_length=400)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE,blank=True, null=True)
    creado = models.DateTimeField('creado',auto_now_add=True)
    actualizado = models.DateTimeField('actualizado',auto_now=True)
    
    class Meta:
        permissions = (
                       ( "familia_obs_crear","Agregar nueva observacion a una familia"),
                       ( "familia_obs_editar","Editar una observacion"),
                       ( "familia_obs_borrar","Eliminar una observacion"),
                       ( "familia_obs_ver","Ver una observacion" ),
                      )

    def __str__(self):
        return  "{}, {}".format(self.familia.familia_crm_id,self.pk)

