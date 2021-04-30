import datetime
from django import forms
from .models import Familia, Socio, Observaciones

# Año de inicio para combo seleccionable para fecha de nacimiento
def init_year_birthday():
    start = (datetime.date.today().year -99)
    return start

# Año de de fin para combo seleccionable para fecha de nacimiento
def end_year_birthday():
    end = (datetime.date.today().year - 6)
    return end

class DateInput(forms.DateInput):
    input_type = 'date'


class SocioForm(forms.ModelForm):

    nombres = forms.CharField(max_length=50,min_length=4,required=True)
    apellidos = forms.CharField(max_length=50,min_length=4,required=True)
    fecha_nacimiento = forms.DateField(required=False,widget = forms.SelectDateWidget(years=range(init_year_birthday(), end_year_birthday())) )
    dni = forms.IntegerField(max_value=999999999999999,help_text='maximo 15 digitos', required=True)

    class Meta:
        model = Socio
        fields = ('nombres', 'apellidos', 'dni', 'fecha_nacimiento',
                  'familia', 'categoria', 'rama')
        

class FamiliaForm(forms.ModelForm):

    crm_id = forms.IntegerField(label="Familia ID")
    familia_crm_id = forms.CharField(label="Familia")
    direccion_calle = forms.CharField(label="Calle")
    direccion_numero = forms.CharField(label="Numero")
    direccion_depto = forms.CharField(label="Depto/timbre")
    direccion_localidad = forms.CharField(label="Localidad")
    direccion_provincia = forms.CharField(label="Provincia")
    contacto = forms.CharField(label="Datos de Contacto",widget=forms.Textarea(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Familia
        fields = ('crm_id', 'familia_crm_id', 'direccion_calle', 'direccion_numero',
                  'direccion_depto', 'direccion_localidad', 'direccion_provincia','contacto')
        
        
class ObservacionForm(forms.ModelForm):

    detalle = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Observaciones
        fields = ('detalle', 'familia')
        
