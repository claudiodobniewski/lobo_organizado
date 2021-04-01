from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from socios.models import Familia, Socio, Observaciones
from cuotas.models import CuotaSocialFamilia,CuotaPago

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the cuotas index.")

def nuevo_pago(request, familia_id):


    return HttpResponse("Hello, world. ACA VA PANTALLA PAGO NUEVA CUOTA.")
    #render(request, 'socios/familia_detalle.html', {'familia': familia_socios,'socios':socios,'cuotas':plan_de_pago,'pagos':pagos, 'observaciones':observaciones})