from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Familia, Socio, Observaciones
from cuotas.models import CuotaSocialFamilia,CuotaPago
from django.template.defaulttags import register
from django.template.defaultfilters import stringfilter
from urllib.parse import unquote

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

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

@register.filter(name='unquote_raw')
def unquote_raw(value):
    return unquote(value)

def familia_index(request):

    lista_familias = Familia.objects.all()

    socios = Socio.objects.all()

    
    familia_estadisticas_socios = {}

    categorias = {k:0 for k,categoria in Socio.CATEGORIAS_CHOISES }

    print(categorias)
    for socio in socios:

        #print("familia:{} categoria:{} claves:{}".format(socio.familia.id,socio.categoria,familia_estadisticas_socios.keys()) )
        
        if socio.familia.id not in familia_estadisticas_socios.keys():
            #print("seteando dict categorias")
            familia_estadisticas_socios[socio.familia.id] = {'categorias_counter': categorias.copy(), 'familia':socio.familia }


        #print("familia:{} categoria:{} claves:{}".format(socio.familia.id,socio.categoria,familia_estadisticas_socios.keys()) )
        #print(familia_estadisticas_socios)
        familia_estadisticas_socios[socio.familia.id]['categorias_counter'][socio.categoria] += 1

    print(familia_estadisticas_socios)

    
    return render(request, 'socios/familia_listado.html', {'familias': lista_familias,'familias_categorias':familia_estadisticas_socios} )

def familia_detalle(request, familia_id, error_message=''):
    
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
        observaciones = Observaciones.objects.filter(familia_id=familia_socios.id)
        print(pagos)
        print("-------------")
    except Exception as err:
        raise Http404("Unexpected error: {0}".format(err))
    return render(request, 'socios/familia_detalle.html', {'familia': familia_socios,'socios':socios,'cuotas':plan_de_pago,'pagos':pagos, 'observaciones':observaciones, 'error_message': error_message })

def familia_observacion_editar(request, observacion_id):
    return HttpResponse("Hello, world. ACA VA OBSERVACIONES EDITAR.")

def familia_observacion_borrar(request, observacion_id):
    return HttpResponse("Hello, world. ACA VA OBSERVACIONES BORRAR.")