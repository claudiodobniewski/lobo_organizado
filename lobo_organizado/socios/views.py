from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from cuotas.models import CuotaSocialFamilia,CuotaPago
from django.template.defaulttags import register
from urllib.parse import unquote

from .forms import SocioForm
from .models import Familia, Socio, Observaciones

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

def socio_nuevo(request,familia_id):
    print("Socio nuevo a familia {}".format(familia_id))
    familia_socios = Familia.objects.get(pk=familia_id)
    socio = Socio(familia_id=familia_socios)
    print("Socio --> {}".format(socio))
    if request.method == "POST":
        form = SocioForm(request.POST,instance=socio)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            print("CAMINO 1 familia {}".format(familia_id))
            redirect('socios:familia_detalle', familia_id=familia_id)

    else:
        print("CAMINO 2 SOCIO NUEVO - familia  {} - {}".format(familia_id,familia_socios.familia_crm_id))

        form = SocioForm(instance=socio)
        print("From:{}".format(form))
    return render(request, 'socios/socio_nuevo.html', {'form': form, "familia": familia_socios })

def socio_editar(request, socio_id):
    
    print("Socio edicion  {}".format(socio_id))
    socio = Socio.objects.get(pk=socio_id)
    #post = get_object_or_404(Socio, pk=socio_id)
    familia_socios = Familia.objects.get(pk=socio.familia.id)
    if request.method == "POST":
        form = SocioForm(request.POST, instance=socio)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            print("CAMINO 1 edicion socio {} - familia {}".format(socio.id,familia_socios.id))
            redirect('socios:familia_detalle', familia_id=familia_socios.id)

    else:
        print("CAMINO 2 edicion socio {} - familia {}".format(socio.id,familia_socios.id))
        form = SocioForm(instance=socio)
        print("From:{}".format(form))
    return render(request, 'socios/socio_nuevo.html', {'form': form, "familia": familia_socios })

def socio_borrar(request, socio_id):
    pass

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

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


@register.filter(name='unquote_raw')
def unquote_raw(value):
    return unquote(value)
