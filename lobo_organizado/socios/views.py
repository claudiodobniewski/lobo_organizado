from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Familia, Socio
from cuotas.models import CuotaSocialFamilia,CuotaPago

def index(request):
    return familias_index(request)

def socio_index(request):

    lista_socios = Socio.objects.all()
    
    print(lista_socios)
    return render(request, 'socios/socios_listado.html', {'socios': lista_socios})

def socio_detalle(request, socio_id):
    
    try:
        socio = Socio.objects.get(pk=socio_id)
        print("Detalle socio:" + socio.apellidos +", "+ socio.nombres)
    except Exception as err:
        raise Http404("Unexpected error: {0}".format(err))
    return render(request, 'socios/socio_detalle.html', {'socio':socio})

def familia_index(request):

    lista_familias = Familia.objects.all()
    
    print(lista_familias)
    return render(request, 'socios/familia_listado.html', {'familias': lista_familias})

def familia_detalle(request, familia_id):
    
    try:
        familia_socios = Familia.objects.get(pk=familia_id)
        socios = Socio.objects.filter(familia_id=familia_socios.id)
        print(socios)

        plan_de_pago = CuotaSocialFamilia.objects.filter(familia_id=familia_socios.id)
       
        print(plan_de_pago)
        print("-------------")
        pagos = CuotaPago.objects.filter(familia_id=familia_socios.id)
        print(pagos)
        print("-------------")
    except Exception as err:
        raise Http404("Unexpected error: {0}".format(err))
    return render(request, 'socios/familia_detalle.html', {'familia': familia_socios,'socios':socios,'cuotas':plan_de_pago,'pagos':pagos})

