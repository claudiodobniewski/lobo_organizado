from django import forms
from django.forms.widgets import DateInput

from .models import CuotaPago,CuotaSocialFamilia,PlanDePago

class DateInput(forms.DateInput):
    input_type = 'date'
class CuotaPagoForm(forms.ModelForm):

    class Meta:
        model = CuotaPago
        fields = ('importe', 'fecha_cobro', 'aplica_pago_plan', 'familia')

class CuotaSocialFamiliaForm(forms.ModelForm):

    class Meta:
        model = CuotaSocialFamilia
        fields = ('vencimiento', 'importe_cuota',
                  'plan_de_pago', 'familia')
    pass

class PlanDePagoForm(forms.ModelForm):

    vto_primera_cuota = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control'}))
    class Meta:
        model = PlanDePago
        fields = ('crm_id', 'nombre', 'descripcion',
                  'cantidad_cuotas', 'vto_primera_cuota','importe_cuota')
        
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
    pass