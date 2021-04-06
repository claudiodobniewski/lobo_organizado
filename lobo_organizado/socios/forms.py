from django import forms

from .models import  Socio,Familia


class SocioForm(forms.ModelForm):

    class Meta:
        model = Socio
        fields = ('nombres', 'apellidos','dni','fecha_nacimiento','familia','categoria','rama')


        