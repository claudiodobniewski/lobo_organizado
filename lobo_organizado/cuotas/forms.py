from django import forms
from django.forms.widgets import DateInput

from .models import CuotaPago,CuotaSocialFamilia,PlanDePago

class DateInput(forms.DateInput):
    input_type = 'date'
class CuotaPagoForm(forms.ModelForm):


    fecha_cobro = forms.DateField(widget = forms.SelectDateWidget )
    importe = forms.DecimalField()

    class Meta:
        model = CuotaPago
        fields = ('importe', 'fecha_cobro', 'aplica_pago_plan', 'familia')



class CuotaSocialFamiliaForm(forms.ModelForm):

    vencimiento = forms.DateField()
    class Meta:
        model = CuotaSocialFamilia
        fields = ('vencimiento', 'importe_cuota',
                  'plan_de_pago', 'familia')
        
    

class PlanDePagoForm(forms.ModelForm):

    vto_primera_cuota = forms.DateField()
    class Meta:
        model = PlanDePago
        fields = ('crm_id', 'nombre', 'descripcion',
                  'cantidad_cuotas', 'vto_primera_cuota','importe_cuota')
        
    