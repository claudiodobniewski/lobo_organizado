from django import forms
from .models import  Socio,Observaciones

class DateInput(forms.DateInput):
    input_type = 'date'
class SocioForm(forms.ModelForm):

    fecha_nacimiento = forms.DateField(widget=DateInput())
    class Meta:
        model = Socio
        fields = ('nombres', 'apellidos','dni','fecha_nacimiento','familia','categoria','rama')

class ObservacionForm(forms.ModelForm):

    detalle = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Observaciones
        fields = ('detalle', 'familia')



        