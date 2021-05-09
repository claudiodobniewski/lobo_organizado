
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from django.template.defaulttags import register
from urllib.parse import unquote

from .forms import 
from .models import Familia, Socio, Observaciones



def observacion_editar(request, observacion_id):
    
    logger.debug("Socio edicion  {}".format(observacion_id))
    observacion = Socio.objects.get(pk=observacion_id)
    #post = get_object_or_404(Socio, pk=observacion_id)
    familia_observacions = Familia.objects.get(pk=observacion.familia.id)
    

    if request.method == "POST":
        form = SocioForm(request.POST, instance=observacion)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            logger.debug("CAMINO 1 edicion observacion {} - familia {}".format(observacion.id,familia_observacions.id))
            return redirect('observacions:familia_detalle', familia_id=familia_observacions.id)
    else:
        logger.debug("CAMINO 2 edicion observacion {} - familia {}".format(observacion.id,familia_observacions.id))
        form = SocioForm(instance=observacion)
        #logger.debug("From:{}".format(form))
    
    op_title='Editar Socio'
    boton_aceptar='Guardar cambios'
    boton_cancelar='Descartar cambios y regresar a detalle familia {}'.format(familia_observacions.familia_crm_id)

    logger.debug("Socio editar END")
    return render(request, 'observacions/observacion_nuevo.html', {'form': form, "familia": familia_observacions, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })

def observacion_borrar(request, observacion_id):
    
    logger.debug("Socio borrar  {}".format(observacion_id))
    observacion = Socio.objects.get(pk=observacion_id)
    #post = get_object_or_404(Socio, pk=observacion_id)
    familia_observacions = Familia.objects.get(pk=observacion.familia.id)

   
    if request.method == "POST":
        form = SocioForm(request.POST, instance=observacion)
        #observacion_id = int(request.POST.get('observacion_id'))  
        observacion = Socio.objects.get(id=observacion_id)       
        observacion.delete()
        logger.debug("CAMINO 1 borrar observacion {} - familia {}".format(observacion.id,familia_observacions.id))
        return redirect('observacions:familia_detalle', familia_id=familia_observacions.id)

    else:
        logger.debug("CAMINO 2 borrar observacion {} - familia {}".format(observacion.id,familia_observacions.id))
        form = SocioForm(instance=observacion)
        form.fields['nombres'].disabled = True
        form.fields['apellidos'].disabled = True
        form.fields['dni'].disabled = True
        form.fields['fecha_nacimiento'].disabled = True
        form.fields['categoria'].disabled = True
        form.fields['rama'].disabled = True
        form.fields['familia'].disabled = True
        logger.debug("From:{}".format(form))
    logger.debug("Socio borrar END")
    return render(request, 'observacions/observacion_borrar.html', {'form': form, "familia": familia_observacions })

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

def familia_index(request):

    lista_familias = Familia.objects.all()

    observacions = Socio.objects.all()

    
    familia_estadisticas_observacions = {}

    categorias = {k:0 for k,categoria in Socio.CATEGORIAS_CHOISES }

    logger.debug(categorias)
    for observacion in observacions:

        #logger.debug("familia:{} categoria:{} claves:{}".format(observacion.familia.id,observacion.categoria,familia_estadisticas_observacions.keys()) )
        
        if observacion.familia.id not in familia_estadisticas_observacions.keys():
            #logger.debug("seteando dict categorias")
            familia_estadisticas_observacions[observacion.familia.id] = {'categorias_counter': categorias.copy(), 'familia':observacion.familia }


        #logger.debug("familia:{} categoria:{} claves:{}".format(observacion.familia.id,observacion.categoria,familia_estadisticas_observacions.keys()) )
        #logger.debug(familia_estadisticas_observacions)
        familia_estadisticas_observacions[observacion.familia.id]['categorias_counter'][observacion.categoria] += 1

    logger.debug(familia_estadisticas_observacions)

    
    return render(request, 'observacions/familia_listado.html', {'familias': lista_familias,'familias_categorias':familia_estadisticas_observacions} )

def familia_detalle(request, familia_id, error_message=''):
    
    try:
        familia_observacions = Familia.objects.get(pk=familia_id)
        observacions = Socio.objects.filter(familia_id=familia_observacions.id)
        logger.debug(observacions)

        plan_de_pago = CuotaSocialFamilia.objects.filter(familia_id=familia_observacions.id)
       
        logger.debug(plan_de_pago)
        logger.debug("-------------")
        pagos = CuotaPago.objects.filter(familia_id=familia_observacions.id)
        logger.debug(pagos)
        logger.debug("-------------")
        observaciones = Observaciones.objects.filter(familia_id=familia_observacions.id)
        logger.debug(pagos)
        logger.debug("-------------")
    except Exception as err:
        raise Http404("Unexpected error: {0}".format(err))
    return render(request, 'observacions/familia_detalle.html', {'familia': familia_observacions,'observacions':observacions,'cuotas':plan_de_pago,'pagos':pagos, 'observaciones':observaciones, 'error_message': error_message })

def familia_observacion_editar(request, observacion_id):
    return HttpResponse("Hello, world. ACA VA OBSERVACIONES EDITAR.")

def familia_observacion_borrar(request, observacion_id):
    return HttpResponse("Hello, world. ACA VA OBSERVACIONES BORRAR.")


@register.filter(name='unquote_raw')
def unquote_raw(value):
    return unquote(value)
