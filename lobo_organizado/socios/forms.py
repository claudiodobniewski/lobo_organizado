from django import forms
from .models import Familia, Socio, Observaciones


class DateInput(forms.DateInput):
    input_type = 'date'


class SocioForm(forms.ModelForm):

    nombres = forms.CharField(max_length=50,min_length=4,required=True)
    apellidos = forms.CharField(max_length=50,min_length=4,required=True)
    fecha_nacimiento = forms.DateField(required=False,
        widget=DateInput(attrs={'class': 'form-control'}))
    dni = forms.IntegerField(max_value=999999999999999,help_text='maximo 15 digitos', required=True)

    class Meta:
        model = Socio
        fields = ('nombres', 'apellidos', 'dni', 'fecha_nacimiento',
                  'familia', 'categoria', 'rama')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

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
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
class ObservacionForm(forms.ModelForm):

    detalle = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Observaciones
        fields = ('detalle', 'familia')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
