from django import forms
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from cuotas.models import CuotaSocialFamilia,CuotaPago
from django.template.defaulttags import register
from urllib.parse import unquote

from .forms import FamiliaForm, SocioForm, ObservacionForm
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
    #print("Socio --> {}".format(socio))


    if request.method == "POST":
        form = SocioForm(request.POST,instance=socio)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            print("CAMINO 1 familia {}".format(familia_id))
            return redirect('socios:familia_detalle', familia_id=familia_id)
    else:
        print("CAMINO 2 SOCIO NUEVO - familia  {} - {}".format(familia_id,familia_socios.familia_crm_id))

        form = SocioForm(instance=socio)
        #print("From:{}".format(form))
    
    op_title='Nuevo Socio'
    boton_aceptar='Agregar Socio a la Familia'
    boton_cancelar='Descartar cambios y regresar a detalle familia {}'.format(familia_socios.familia_crm_id)

    print("Socio nuevo END")
    return render(request, 'socios/socio_nuevo.html', {'form': form, "familia": familia_socios, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })

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
            return redirect('socios:familia_detalle', familia_id=familia_socios.id)
    else:
        print("CAMINO 2 edicion socio {} - familia {}".format(socio.id,familia_socios.id))
        form = SocioForm(instance=socio)
        #print("From:{}".format(form))
    
    op_title='Editar Socio'
    boton_aceptar='Guardar cambios'
    boton_cancelar='Descartar cambios y regresar a detalle familia {}'.format(familia_socios.familia_crm_id)

    print("Socio editar END")
    return render(request, 'socios/socio_nuevo.html', {'form': form, "familia": familia_socios, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })

def socio_borrar(request, socio_id):
    
    print("Socio borrar  {}".format(socio_id))
    socio = Socio.objects.get(pk=socio_id)
    #post = get_object_or_404(Socio, pk=socio_id)
    familia_socios = Familia.objects.get(pk=socio.familia.id)

   
    if request.method == "POST":
        form = SocioForm(request.POST, instance=socio)
        #socio_id = int(request.POST.get('socio_id'))  
        socio = Socio.objects.get(id=socio_id)       
        socio.delete()
        print("CAMINO 1 borrar socio {} - familia {}".format(socio.id,familia_socios.id))
        return redirect('socios:familia_detalle', familia_id=familia_socios.id)

    else:
        print("CAMINO 2 borrar socio {} - familia {}".format(socio.id,familia_socios.id))
        form = SocioForm(instance=socio)
        form.fields['nombres'].disabled = True
        form.fields['apellidos'].disabled = True
        form.fields['dni'].disabled = True
        form.fields['fecha_nacimiento'].disabled = True
        form.fields['categoria'].disabled = True
        form.fields['rama'].disabled = True
        form.fields['familia'].disabled = True
        print("From:{}".format(form))
    print("Socio borrar END")
    return render(request, 'socios/socio_borrar.html', {'form': form, "familia": familia_socios })

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

def familia_index(request,error_message=''):

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


    return render(request, 'socios/familia_listado.html', {'familias': lista_familias, 'error_message': error_message} )

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

def familia_nuevo(request,familia_id, error_message=''):
    print("Socio nuevo a familia {}".format(familia_id))

    

    if familia_id :
        familia_socios = Familia.objects.get_or_create(pk=familia_id)
        op_title='Editar Familia'
        boton_aceptar='Guardar cambios'
        boton_cancelar='Descartar cambios y regresar a detalle familia {}'.format(familia_socios.familia_crm_id)
    else:
        familia_socios = Familia()
        op_title='Nueva Familia'
        boton_aceptar='Agregar Observacion a la Familia'
        boton_cancelar='Descartar nueva familia y regresas al listado de  familias '
    #print("Socio --> {}".format(observacion))

    if request.method == "POST":
        form = FamiliaForm(request.POST,instance=familia_socios)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            print("CAMINO 1 familia {}".format(familia_socios.pk))
            return redirect('socios:familia_detalle', familia_id=familia_socios.pk)
    else:
        print("CAMINO 2 SOCIO NUEVO - familia  {} - {}".format(familia_id,familia_socios.familia_crm_id))

        form = FamiliaForm(instance=familia_socios)
        #print("From:{}".format(form))
    
    op_title='Nueva Familia'
    boton_aceptar='Generar nueva Familia'
    boton_cancelar='Descartar cambios y regresar a listado de familias.'

    print("Socio nuevo END")
    return render(request, 'socios/familia_nuevo.html', {'form': form, "familia": familia_socios, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })

def familia_observacion_editar(request, observacion_id):
    return HttpResponse("Hello, world. ACA VA OBSERVACIONES EDITAR.")

def familia_observacion_borrar(request, observacion_id):
    return HttpResponse("Hello, world. ACA VA OBSERVACIONES BORRAR.")


def observacion_nuevo(request,familia_id,observacion_id):
    print("Observacion nuevo a familia {}".format(familia_id))

    familia_observacions = Familia.objects.get(pk=familia_id)
    if observacion_id :
        observacion = Observaciones.objects.get(pk=observacion_id)
        op_title='Editar Observacion'
        boton_aceptar='Guardar cambios'
        boton_cancelar='Descartar cambios y regresar a detalle familia {}'.format(familia_observacions.familia_crm_id)
    else:
        observacion = Observaciones(familia_id=familia_observacions)
        op_title='Nueva Observacion'
        boton_aceptar='Agregar Observacion a la Familia'
        boton_cancelar='Descartar nueva observacion y regresar a detalle familia {}'.format(familia_observacions.familia_crm_id)
    #print("Socio --> {}".format(observacion))


    if request.method == "POST":
        form = ObservacionForm(request.POST,instance=observacion)
        form.fields['familia'].disabled = True
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            print("CAMINO 1 familia {}".format(familia_id))
            return redirect('socios:familias', familia_id=familia_id)
    else:
        print("CAMINO 2 SOCIO NUEVO - familia  {} - {}".format(familia_id,familia_observacions.familia_crm_id))

        form = ObservacionForm(instance=observacion)
        form.fields['familia'].disabled = True
        form.fields['familia'].widget = forms.HiddenInput()
        #print("From:{}".format(form))
    
    print("Socio nuevo END")
    return render(request, 'socios/observacion_nuevo.html', {'form': form, "familia": familia_observacions, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })

def observacion_borrar(request, observacion_id):
    
    print("Observacion borrar  {}".format(observacion_id))
    observacion = Observaciones.objects.get(pk=observacion_id)
    #post = get_object_or_404(Socio, pk=socio_id)
    familia_socios = Familia.objects.get(pk=observacion.familia.id)

   
    if request.method == "POST":
        form = ObservacionForm(request.POST, instance=observacion)
        #socio_id = int(request.POST.get('socio_id'))  
        #observacion = Observaciones.objects.get(id=observacion_id)       
        observacion.delete()
        print("CAMINO 1 borrar observacion {} - familia {}".format(observacion.id,familia_socios.id))
        return redirect('socios:familia_detalle', familia_id=familia_socios.id)

    else:
        print("CAMINO 2 borrar socio {} - familia {}".format(observacion.id,familia_socios.id))
        form = ObservacionForm(instance=observacion)
        form.fields['detalle'].disabled = True
        form.fields['familia'].disabled = True
        form.fields['familia'].widget = forms.HiddenInput()
        print("From:{}".format(form))
    print("Observacion borrar END")
    return render(request, 'socios/observacion_borrar.html', {'form': form, "familia": familia_socios })

@register.filter(name='unquote_raw')
def unquote_raw(value):
    return unquote(value)
