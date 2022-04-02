import datetime
from django import forms
from django.forms.widgets import DateInput

from .models import CuotaPago,CuotaSocialFamilia,PlanDePago

# Año de inicio para combo seleccionable para fecha de pago
def init_year_pay():
    start = (datetime.date.today().year -2)
    return start

# Año de de fin para combo seleccionable para fecha de pago
def end_year_pay():
    end = (datetime.date.today().year + 1)
    return end

class DateInput(forms.DateInput):
    input_type = 'date'
class CuotaPagoForm(forms.ModelForm):

    fecha_cobro = forms.DateField(widget = forms.SelectDateWidget(years=range(init_year_pay(), end_year_pay()) ) )
    importe = forms.DecimalField()
    #hash = forms.UUIDField( widget=forms.TextInput(attrs={'readonly':'readonly'}),required=False)
    hash = forms.TextInput( )
    

    def __init__(self, *args, **kwargs):
         super(CuotaPagoForm, self).__init__(*args, **kwargs)
         self.fields['hash'].widget.attrs['readonly'] = True

    def __set_readonly( self ):
        for field in self.fields:                
            self.fields[field].required = False
            self.fields[field].widget.attrs['disabled'] = 'disabled'
            
    class Meta:
        model = CuotaPago
        #readonly_fields = ['hash',]
        fields = ('importe', 'fecha_cobro','forma_de_pago','comprobante','aplica_pago_plan', 'familia','hash')


class CuotaSocialFamiliaForm(forms.ModelForm):

    vencimiento = forms.DateField(widget = forms.SelectDateWidget(years=range(init_year_pay(), end_year_pay()) ) )
    class Meta:
        model = CuotaSocialFamilia
        fields = ('vencimiento', 'importe_cuota',
                  'plan_de_pago', 'familia')
        
    

class PlanDePagoForm(forms.ModelForm):

    vto_primera_cuota = forms.DateField(widget = forms.SelectDateWidget(years=range(init_year_pay(), end_year_pay()) ) )
    class Meta:
        model = PlanDePago
        fields = ('crm_id', 'nombre', 'descripcion',
                  'cantidad_cuotas', 'vto_primera_cuota','importe_cuota')
        
class ListadoCobranzaForm(forms.ModelForm):


    class Meta:
        fields = ('familia', 'plan_de_pago','cuotas','cuotas_vencidas','balance')