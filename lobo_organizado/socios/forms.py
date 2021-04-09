from django import forms
from .models import Familia, Socio, Observaciones


class DateInput(forms.DateInput):
    input_type = 'date'


class SocioForm(forms.ModelForm):

    fecha_nacimiento = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control'}))

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

    contacto = forms.CharField(widget=forms.Textarea(
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
