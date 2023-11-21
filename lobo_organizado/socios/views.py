import datetime
from django import forms
from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from django.template.defaulttags import register
from urllib.parse import unquote
from django.utils.http import urlquote
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.paginator import Paginator
from django.views.generic import ListView
import inspect ,logging
import cuotas.models as app_cuotas
from cuotas.models import CuotaSocialFamilia,CuotaPago,PlanDePago
from reportes.views import reporte_estado_familias,reporte_familia_pdf
import copy
from django.db.models import Q

from django.contrib.auth.models import Permission

from .forms import FamiliaForm, SocioForm, ObservacionForm
from .models import Familia, Socio, Observaciones
from itertools import chain

logger = logging.getLogger('project.lobo.organizado')

#ver si esto es util, no se utiliza, lo puse probando paginado
class FamiliaListView(ListView):
    paginate_by = 2
    model = Familia

def login_url_with_redirect(request):
    logger.debug('Something went wrong!')
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    login_url = settings.LOGIN_URL
    path = urlquote(request.get_full_path())
    url = '%s?%s=%s' % (settings.LOGIN_URL, REDIRECT_FIELD_NAME, path)
    return {'login_url': url}
    
def index(request):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
    return render(request, 'index.html', {})

def socio_index(request):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
    lista_socios = Socio.objects.all()
    
    logger.debug(lista_socios)
    return render(request, 'socios/socios_listado.html', {'socios': lista_socios})

def socio_detalle(request, socio_id):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
    try:
        socio = Socio.objects.get(pk=socio_id)
        logger.debug("Detalle socio:" + socio.apellidos +", "+ socio.nombres)
    except Exception as err:
        raise Http404("Unexpected error: {0}".format(err))
    return render(request, 'socios/socio_detalle.html', {'socio':socio})

def socio_nuevo(request,familia_id):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
    logger.debug("Socio nuevo a familia {}".format(familia_id))
    familia_socios = Familia.objects.get(pk=familia_id)
    socio = Socio(familia_id=familia_socios)
    #logger.debug("Socio --> {}".format(socio))


    if request.method == "POST":
        form = SocioForm(request.POST,instance=socio)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            logger.debug("CAMINO 1 familia {}".format(familia_id))
            return redirect('socios:familia_detalle', familia_id=familia_id)
    else:
        logger.debug("CAMINO 2 SOCIO NUEVO - familia  {} - {}".format(familia_id,familia_socios.familia_crm_id))

        form = SocioForm(instance=socio)
        #logger.debug("From:{}".format(form))
    
    op_title='Nuevo Socio'
    boton_aceptar='Agregar Socio a la Familia'
    boton_cancelar='Descartar cambios y regresar a detalle familia {}'.format(familia_socios.familia_crm_id)

    logger.debug("Socio nuevo END")
    return render(request, 'socios/socio_nuevo.html', {'form': form, "familia": familia_socios, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })

def socio_editar(request, socio_id):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("Socio edicion  {}".format(socio_id))
    socio = Socio.objects.get(pk=socio_id)
    #post = get_object_or_404(Socio, pk=socio_id)
    familia_socios = Familia.objects.get(pk=socio.familia.id)
    

    if request.method == "POST":
        form = SocioForm(request.POST, instance=socio)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            logger.debug("CAMINO 1 edicion socio {} - familia {}".format(socio.id,familia_socios.id))
            return redirect('socios:familia_detalle', familia_id=familia_socios.id)
    else:
        logger.debug("CAMINO 2 edicion socio {} - familia {}".format(socio.id,familia_socios.id))
        form = SocioForm(instance=socio)
        #logger.debug("From:{}".format(form))
    
    op_title='Editar Socio'
    boton_aceptar='Guardar cambios'
    boton_cancelar='Descartar cambios y regresar a detalle familia {}'.format(familia_socios.familia_crm_id)

    logger.debug("Socio editar END")
    return render(request, 'socios/socio_nuevo.html', {'form': form, "familia": familia_socios, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })

def socio_borrar(request, socio_id):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("Socio borrar  {}".format(socio_id))
    socio = Socio.objects.get(pk=socio_id)
    #post = get_object_or_404(Socio, pk=socio_id)
    familia_socios = Familia.objects.get(pk=socio.familia.id)

   
    if request.method == "POST":
        form = SocioForm(request.POST, instance=socio)
        #socio_id = int(request.POST.get('socio_id'))  
        socio = Socio.objects.get(id=socio_id)       
        socio.delete()
        logger.debug("CAMINO 1 borrar socio {} - familia {}".format(socio.id,familia_socios.id))
        return redirect('socios:familia_detalle', familia_id=familia_socios.id)

    else:
        logger.debug("CAMINO 2 borrar socio {} - familia {}".format(socio.id,familia_socios.id))
        form = SocioForm(instance=socio)
        form.fields['nombres'].disabled = True
        form.fields['apellidos'].disabled = True
        form.fields['dni'].disabled = True
        form.fields['fecha_nacimiento'].disabled = True
        form.fields['categoria'].disabled = True
        form.fields['rama'].disabled = True
        form.fields['familia'].disabled = True
        logger.debug("From:{}".format(form))
    logger.debug("Socio borrar END")
    return render(request, 'socios/socio_borrar.html', {'form': form, "familia": familia_socios })

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

def familia_index(request,error_message=''):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    # BUSQUEDA
    current_user = request.user
    if request.method == 'GET': # If the form is submitted
        search_query = request.GET.get('search_box', None)
        # Reporte PDF options
        report_export_on = request.GET.get('report_export_on', False) # generate and download report
        report_export_all = request.GET.get('report_export_all', False) # Report must include all records? True= yes, False=only current page.

    if search_query:

        busqueda_familias_por_familia = Familia.objects.filter( Q(crm_id__icontains=search_query) | Q(familia_crm_id__icontains=search_query) ) 
        
        busqueda_familias_por_socios = Socio.objects.filter(Q(nombres__icontains=search_query) | Q(apellidos__icontains=search_query)  )
        familias_por_socios_ids = [socio.familia.id for socio in busqueda_familias_por_socios ]
        
        lista_familias = (Familia.objects.filter( id__in = familias_por_socios_ids).distinct() | busqueda_familias_por_familia.distinct() ).order_by('familia_crm_id')
        print("lista_familias *** {}".format(lista_familias))
    
    else:
        lista_familias = Familia.objects.all().order_by('familia_crm_id')
    print("GET:{} POST:{}  search_query:{}  FAMILIAS:{}".format(request.GET.get('search_box', None),request.POST.get('search_box', None),search_query,lista_familias ))
    
    # Paginacion
    if report_export_all:
        paginator = Paginator(lista_familias, len(lista_familias)) # Show x contacts per page.
    else:
        paginator = Paginator(lista_familias, 10) # Show x contacts per page.
    page_number = request.GET.get('page')
    print("page_number {}".format(page_number))
    if paginator.count:
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None

    print("page_obj {}".format(page_obj))

    ###

    categorias = {k:0 for k,categoria in Socio.CATEGORIAS_CHOISES }

    logger.debug(categorias)

    for familia in lista_familias:
        
        #print(familia)
        socios_familia = Socio.objects.filter(familia=familia.id)
        beneficiarios = 0
        dirigentes = 0
        otros = 0
        manada = 0
        unidad = 0
        caminantes = 0
        rovers = 0
        #print("Socios : {}".format(socios_familia))
        

        #################

        for socio in socios_familia:
            #print("Socio:{}#{}#{}".format(socio.pk,socio.nombres,socio.categoria))
            if socio.categoria == 1:
                beneficiarios += 1
                if socio.rama == 1:
                    manada += 1
                elif socio.rama == 2:
                    unidad += 1
                elif socio.rama == 3:
                    caminantes += 1
                elif socio.rama == 4:
                    rovers += 1
            elif socio.categoria == 2:
                dirigentes += 1
            elif socio.categoria > 0:
                otros += 1

        familia.stat_socios = len(copy.copy(socios_familia))
        familia.stat_beneficiarios = copy.copy(beneficiarios)
        familia.stat_dirigentes = copy.copy(dirigentes)
        familia.stat_otros = copy.copy(otros)
        familia.stat_rama_manada = copy.copy(manada)
        familia.stat_rama_unidad = copy.copy(unidad)
        familia.stat_rama_caminantes = copy.copy(caminantes)
        familia.stat_rama_rovers = copy.copy(rovers)

        ###

    if report_export_on:

        filter_info = {
            "search_query" : search_query,
        }

        report_export_on = False
        report_export_all = False
        return reporte_estado_familias(current_user,page_obj, filter_info)

    #return test_report_familias_listado(page_obj)
    return render(request, 'socios/familia_listado.html', {'familias': lista_familias, 'error_message': error_message,'page_obj': page_obj, "search_query": search_query} )

def familia_detalle(request, familia_id, error_message='',views_export_on='FALSE'):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("familia_id:{} error_message:{} views_export_on:{}".format(familia_id, error_message,views_export_on))
    user = request.user
    if not user.is_anonymous:
        perm_tuple = [(x.id, x.name,x.codename) for x in Permission.objects.filter(user=user)]
        #perms = Permission.objects.filter(user=user)
        logger.debug("USUARIO {} PERMISOS {}".format(user,perm_tuple) )
    else:
        logger.debug("Usuario anonimo....")
    
    

    try:
        familia_socios = Familia.objects.get(pk=familia_id)
        socios = Socio.objects.filter(familia_id=familia_socios.id)

        cuota_social = CuotaSocialFamilia.objects.filter(familia_id=familia_socios.id,deleted=False)

        pagos = CuotaPago.objects.filter(familia_id=familia_socios.id,deleted=False)

        observaciones = Observaciones.objects.filter(familia_id=familia_socios.id)

        # cuotas_todas,cuotas_por_plan,cuotas_vencidas,cuotas_suma,pagos_percibidos_queryset,pagos_percibidos_plan,pagos_percibidos_suma
        # TODO discriminar cuotas vencidas, importes pagados POR PLAN y sumar el total, para mejor detalle
        cuotas = app_cuotas.cuotas_queryset(familia_id)
        cuotas_ya_vencidas = app_cuotas.cuotas_vencidas(cuotas,datetime.date.today())
        cuotas_vencidas_importe = app_cuotas.cuotas_suma(cuotas_ya_vencidas)
        
        pagos_totales = app_cuotas.pagos_percibidos_queryset(familia_id)
        pagos_ya_percibidos_suma = app_cuotas.pagos_percibidos_suma(pagos_totales)

        # ahora no es urgente, pero a futuro seria bueno listar los totales de cuotas por plan (si existiera mas de un plan en el año en curso o tuviera deuda de años anteriores)
        #planes_cuotas = PlanDePago.objects.all()
        #cuotas_por_plan =  {x.id: app_cuotas.cuotas_por_plan(cuotas,x.id,False) for x in planes_cuotas }

        logger.debug("Cuotas : {} cuotas_vencidas:{} cuotas_vencidas_suma:{} pagos:{} pagos_suma:{}".format(cuotas,cuotas_ya_vencidas,cuotas_vencidas_importe,pagos_totales,pagos_ya_percibidos_suma))

    except Exception as err:
        raise Http404("Unexpected error: {0}".format(err))

    
    logger.debug("FAMILIA DETALLE GET :{}".format( request.GET.dict()) )
    #views_export_on=request.GET.get('views_export_on', None)

    if views_export_on == 'PDF':
        logger.debug("EXPORT FAMILIA DETALLE TO PDF" )
        return reporte_familia_pdf(data = {
            'usuario': user,
            'familia': familia_socios,
            'socios':socios,
            'cuotas':cuota_social,
            'cuotas_vencidas': cuotas_ya_vencidas,
            'cuotas_vencidas_suma': cuotas_vencidas_importe,
            #'cuotas_por_plan': cuotas_por_plan,
            'pagos':pagos,
            'pagos_suma': pagos_ya_percibidos_suma,
            'observaciones':observaciones
        }
        )

    return render(request, 
    'socios/familia_detalle.html',
     {
        'familia': familia_socios,
        'socios':socios,
        'cuotas':cuota_social,
        'cuotas_vencidas': cuotas_ya_vencidas,
        'cuotas_vencidas_suma': cuotas_vencidas_importe,
        #'cuotas_por_plan': cuotas_por_plan,
        'pagos':pagos,
        'pagos_suma': pagos_ya_percibidos_suma,
        'observaciones':observaciones,
        'error_message': error_message
    })

def familia_nuevo(request,familia_id, error_message=''):
    

    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
    logger.debug("Nueva familia {}".format(familia_id))
    crm_id_offer = False

    if familia_id :
        familia_socios = Familia.objects.get(pk=familia_id)
        logger.debug("Familia  nueva llego el form {} ".format(familia_socios) )
        op_title='Editar Familia'
        boton_aceptar='Guardar cambios'
        boton_cancelar='Descartar cambios y regresar a detalle familia {}'.format(familia_socios)
        boton_cancelar='Descartar cambios y regresar a detalle familia {}'.format(familia_socios.familia_crm_id)
        error_message='Operacion Editar Familia cancelada'
    else:
        #crm_id = form.cleaned_data['crm_id']
        familia_id=0
        familia_socios = Familia()

        crm_id_max = Familia.objects.aggregate(Max('crm_id'))
        
        if crm_id_max['crm_id__max']:
            crm_id_offer=crm_id_max['crm_id__max'] + 1
        else:
            crm_id_offer = 1

        logger.debug("Familia nueva crm_id_offer {} ".format(crm_id_offer) )
        #familia_socios = Familia.objects.create()

        #familia_socios.crm_id = crm_id_max['crm_id__max'] + 1
        #logger.debug("Maximo CRM a este momento:{}".format(1+crm_id_max['crm_id__max']))
        op_title='Nueva Familia'
        boton_aceptar='Agregar nueva Familia'
        boton_cancelar='Descartar nueva familia y regresas al listado de  familias '
        error_message='Operacion Nueva Familia cancelada'
    logger.debug("Familia Nueva --> {}".format(familia_socios))

    if request.method == "POST":
        form = FamiliaForm(request.POST,instance=familia_socios)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            logger.debug("CAMINO 1 familia {}".format(familia_socios.pk))
            return redirect('socios:familia_detalle', familia_id=familia_socios.pk)
    else:
        logger.debug("CAMINO 2 FAMILIA NUEVO - familia  {} - {}".format(familia_id,familia_socios.pk))

        # TODO reemplazar por default data lo de cmr_id_offer
        # default_data = {'crm_id': crm_id_offer, 'url': 'http://'}
        # f = CommentForm(default_data, auto_id=False)
        if not familia_socios.crm_id:
            familia_socios.crm_id = crm_id_offer
        form = FamiliaForm(instance=familia_socios)
        logger.debug("From:{}".format(form))
    
    
    
    #op_title='Nueva Familia'
    #boton_aceptar='Generar nueva Familia'
    #boton_cancelar='Descartar cambios y regresar a listado de familias.'
    dict_template = {'form': form, "familia": familia_socios, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title, 'error_message': error_message, 'crm_id_offer': crm_id_offer, 'familia_id': familia_id }
    logger.debug("Familia  nuevo END {} ".format(dict_template) )
    return render(request, 'socios/familia_nuevo.html', dict_template)

def borrar_borrar(request, familia_id):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("Socio borrar  {}".format(socio_id))
    socio = Socio.objects.get(pk=socio_id)
    #post = get_object_or_404(Socio, pk=socio_id)
    familia_socios = Familia.objects.get(pk=socio.familia.id)

   
    if request.method == "POST":
        form = SocioForm(request.POST, instance=socio)
        #socio_id = int(request.POST.get('socio_id'))  
        socio = Socio.objects.get(id=socio_id)       
        socio.delete()
        logger.debug("CAMINO 1 borrar socio {} - familia {}".format(socio.id,familia_socios.id))
        return redirect('socios:familia_detalle', familia_id=familia_socios.id)

    else:
        logger.debug("CAMINO 2 borrar socio {} - familia {}".format(socio.id,familia_socios.id))
        form = SocioForm(instance=socio)
        form.fields['nombres'].disabled = True
        form.fields['apellidos'].disabled = True
        form.fields['dni'].disabled = True
        form.fields['fecha_nacimiento'].disabled = True
        form.fields['categoria'].disabled = True
        form.fields['rama'].disabled = True
        form.fields['familia'].disabled = True
        logger.debug("From:{}".format(form))
    logger.debug("Socio borrar END")
    return render(request, 'socios/socio_borrar.html', {'form': form, "familia": familia_socios })

def observacion_nuevo(request,familia_id,observacion_id):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("Observacion nuevo a familia {}".format(familia_id))

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
    #logger.debug("Socio --> {}".format(observacion))


    if request.method == "POST":
        form = ObservacionForm(request.POST,instance=observacion)
        form.fields['familia'].disabled = True
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            logger.debug("CAMINO 1 familia {}".format(familia_id))
            return redirect('socios:familia_detalle', familia_id=familia_id)
    else:
        logger.debug("CAMINO 2 SOCIO NUEVO - familia  {} - {}".format(familia_id,familia_observacions.familia_crm_id))

        form = ObservacionForm(instance=observacion)
        form.fields['familia'].disabled = True
        form.fields['familia'].widget = forms.HiddenInput()
        #logger.debug("From:{}".format(form))
    
    logger.debug("Socio nuevo END")
    return render(request, 'socios/observacion_nuevo.html', {'form': form, "familia": familia_observacions, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })

def observacion_borrar(request, observacion_id):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("Observacion borrar  {}".format(observacion_id))
    observacion = Observaciones.objects.get(pk=observacion_id)
    #post = get_object_or_404(Socio, pk=socio_id)
    familia_socios = Familia.objects.get(pk=observacion.familia.id)

   
    if request.method == "POST":
        form = ObservacionForm(request.POST, instance=observacion)
        #socio_id = int(request.POST.get('socio_id'))  
        #observacion = Observaciones.objects.get(id=observacion_id)       
        observacion.delete()
        logger.debug("CAMINO 1 borrar observacion {} - familia {}".format(observacion.id,familia_socios.id))
        return redirect('socios:familia_detalle', familia_id=familia_socios.id)

    else:
        logger.debug("CAMINO 2 borrar socio {} - familia {}".format(observacion.id,familia_socios.id))
        form = ObservacionForm(instance=observacion)
        form.fields['detalle'].disabled = True
        form.fields['familia'].disabled = True
        form.fields['familia'].widget = forms.HiddenInput()
        logger.debug("From:{}".format(form))
    logger.debug("Observacion borrar END")
    return render(request, 'socios/observacion_borrar.html', {'form': form, "familia": familia_socios })

@register.filter(name='unquote_raw')
def unquote_raw(value):
    return unquote(value)
