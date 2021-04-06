from django import forms
from .models import  Socio

class DateInput(forms.DateInput):
    input_type = 'date'
class SocioForm(forms.ModelForm):

    fecha_nacimiento = forms.DateField(widget=DateInput())
    class Meta:
        model = Socio
        fields = ('nombres', 'apellidos','dni','fecha_nacimiento','familia','categoria','rama')



        