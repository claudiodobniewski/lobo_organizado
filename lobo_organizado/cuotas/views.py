#
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect

from .forms import CuotaPagoForm, CuotaSocialFamiliaForm, PlanDePagoForm
from socios.models import Familia
from cuotas.models import PlanDePago,CuotaPago,CuotaSocialFamilia
from decimal import Decimal

from dateutil.relativedelta import relativedelta
import inspect ,logging

logger = logging.getLogger('project.lobo.organizado')

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the cuotas index.")

# creo que se puede borrar
def nuevo_pago(request, familia_id, pago_id=0 ):

    familia_socios = Familia.objects.get(pk=familia_id)

    planes_de_pago = PlanDePago.objects.all()
    planes_de_pago_list = list(planes_de_pago)
    #logger.debug("PLAN DE PAGOS LIST:{}".format(planes_de_pago_list))
    #planes_de_pago_json = simplejson.dumps(planes_de_pago_list)
    #return HttpResponse("Hello, world. ACA VA PANTALLA PAGO NUEVA CUOTA.")

    if not pago_id:
        pago_error_message = 'Cancelado generacion de nuevo pago'
        pago = CuotaPago()
    else:
        pago = CuotaPago.objects.get(id=pago_id)
        
        pago_error_message = 'Cancelado edicion de pago ' # concatenar info del pago cancelado
    logger.debug("error_message [{}] ".format(pago_error_message) )
    return render(request, 'cuotas/crear_editar_pago.html', {'familia': familia_socios,'planes_de_pago':planes_de_pago,'planes_de_pago_list':planes_de_pago_list, 'pago': pago, 'pago_error_message': pago_error_message })

#creoq ue se puede borrar
def procesa_nuevo_pago(request, familia_id):

  
    for param in request.POST:
        logger.debug("Param {}={}".format(param,request.POST[param]))

    selected_family = Familia.objects.get(pk=request.POST['familia_id'])
    selected_plan_de_pago = PlanDePago.objects.get(pk=request.POST['plan_de_pago_id'])
    logger.debug( "URL param:{} => form param:{} plan_id:{}  plan:{} importe={} ".format(familia_id,selected_family.pk,request.POST['plan_de_pago_id'],selected_plan_de_pago,request.POST['importe_cobrado']))
    if selected_family.pk != familia_id:
        logger.debug("no coinciden los id de familia!")
    familia_socios = Familia.objects.get(pk=familia_id)

    planes_de_pago = PlanDePago.objects.get(pk=request.POST['plan_de_pago_id'])

    nuevo_pago = CuotaPago()
    nuevo_pago.importe = request.POST['importe_cobrado']
    nuevo_pago.familia = selected_family
    nuevo_pago.fecha_cobro = request.POST['fecha_cobrado']
    nuevo_pago.aplica_pago_plan = selected_plan_de_pago
    nuevo_pago.save()

    return HttpResponseRedirect(reverse('socios:familia_detalle', args=(selected_family.id,)))

# nuevo pago y edicion
def editar_pago_plan(request, familia_id, pago_id):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.info(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    error_message = ''

    if pago_id:
        pago = CuotaPago.objects.get(pk=pago_id,deleted=False)
    else:
        familia = Familia.objects.get(pk=familia_id)
        plan_de_pago = PlanDePago.objects.get(plan_default=True)
        pago = CuotaPago(familia=familia,aplica_pago_plan=plan_de_pago)
        

    logger.info("{}) Pago {} Familia {} plan de pagos {} ".format(func.co_name,pago.pk,pago.familia.familia_crm_id,pago))

    if request.method == "POST":
        form = CuotaPagoForm(request.POST,instance=pago)
        #form.data.importe = Decimal(form.data['importe'].replace(',','.'))
        # check whether it's valid:
        #fecha_vto_cuota = form.cleaned_data['vto_primera_cuota'] + relativedelta(months=n)

        if form.is_valid() : #and form.cleaned_data['importe'] > Decimal(1.0):
            post = form.save(commit=False)
            post.save()
            return redirect('socios:familia_detalle', familia_id=familia_id  )
        else:
            pago.delete()
            error_message = 'Error en los datos'

    
    form = CuotaPagoForm(instance=pago)
    
    return render(request, 'cuotas/pago_plan_editar.html', {'form': form, 'pago': pago , 'error_message' : error_message })

def borrar_pago_plan(request, familia_id, pago_id):
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.info(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
 # GENERAR DELETE DE PAGO - esto copia el editar_cuota
    pago = CuotaPago.objects.get(pk=pago_id)
    logger.info("FORM DELETE PAGO  {}) Pago {} Familia {} plan de pagos {} ".format(func.co_name,pago.pk,pago.familia.familia_crm_id,pago))

    if request.method == "POST" and 'delete' in request.POST:
        form = CuotaPagoForm(instance=pago)
        #logger.info("FORM DELETE PAGO POST {}) Cuota {} Familia {} plan de pagos {} valid {} ".format(func.co_name,cuota.pk,cuota.familia.familia_crm_id,cuota,form.is_valid()))
        # check whether it's valid:
        #if form.is_valid():
        form.is_valid()
        post = form.save(commit=False)
        post.deleted = True
        post.save()
        logger.info("FORM POST {} IS VALID".format(form))
        return redirect('socios:familia_detalle', familia_id=familia_id  )
        #else:
        #    logger.info("FORM DELETE INVALID PAGO POST {}) Cuota {} Familia {} plan de pagos {} errores {} ".format(func.co_name,cuota.pk,cuota.familia.familia_crm_id,cuota,form.errors))

    
    form = CuotaPagoForm(instance=pago)
    form.fields['importe'].widget.attrs['disabled'] = 'disabled'
    form.fields['fecha_cobro'].widget.attrs['disabled'] = 'disabled'
    form.fields['aplica_pago_plan'].widget.attrs['disabled'] = 'disabled'
    form.fields['familia'].widget.attrs['disabled'] = 'disabled'
    
    #logger.info(" RENDER {}) Cuota {} Familia {} plan de pagos {} ".format(func.co_name,cuota.pk,cuota.familia.familia_crm_id,cuota))
    return render(request, 'cuotas/pago_plan_borrar.html', {'form': form, 'pago': pago })

def nuevo_cuotas_plan_seleccion(request, familia_id):

    familia = Familia.objects.get(pk=familia_id)
    planes_de_pago = PlanDePago.objects.all()

    return render(request, 'cuotas/nuevo_cuotas_plan_seleccion.html', {'familia': familia,'planes_de_pago':planes_de_pago})


def nuevo_cuotas_plan(request, familia_id, plan_pagos_id):

    
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.info(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
    familia = Familia.objects.get(pk=familia_id)
    logger.info("{}) Familia {} plan de pagos {} ".format(func.co_name,familia_id,plan_pagos_id))
    print(request.POST)
    if plan_pagos_id :
        plan_de_pago = PlanDePago.objects.get(pk=plan_pagos_id)
    else:
        plan_de_pago = PlanDePago.objects.get(pk=plan_pagos_id)
    #logger.debug("Socio --> {}".format(socio))

# CUANDO RECIBO UN PLAN CON LAS CUOTAS, RECIBO UN FORM, TENGO QUE GENERAR LAS CUOTAS, NO MODIFICAR EL PLAN!!!!
    if request.method == "POST":
        form = PlanDePagoForm(request.POST,instance=plan_de_pago)
        op_title='Editar Plan de pago'
        boton_aceptar='Guardar cambios a Plan de pago'
        boton_cancelar='Descartar cambios y regresar a Plan de pago {}#{}'.format(plan_de_pago.crm_id,plan_de_pago.nombre)
        form.fields['nombre'].disabled = True
        form.fields['descripcion'].disabled = True
        form.fields['crm_id'].disabled = True
        if form.is_valid():
            #post = form.save(commit=False)
            #post.save()
            print("Recibido para familia {} , sumar {} cuotas de ${} , inicia primera cuota [{}]".format(familia.familia_crm_id,form.cleaned_data['cantidad_cuotas'],form.cleaned_data['importe_cuota'],form.cleaned_data['vto_primera_cuota'] ) )
            logger.debug("CAMINO 1 Plan de Pago {}".format(plan_pagos_id))
            cant_cuotas = int(form['cantidad_cuotas'].value())
            for n in range(cant_cuotas):
                fecha_vto_cuota = form.cleaned_data['vto_primera_cuota'] + relativedelta(months=n)
                cuota_nueva = CuotaSocialFamilia( 
                    vencimiento = fecha_vto_cuota,
                    importe_cuota = form.data['importe_cuota'], 
                    plan_de_pago = plan_de_pago, 
                    familia = familia
                )
                print('Cuota nueva {}'.format(cuota_nueva) )
                cuota_nueva.save()

            return redirect('socios:familia_detalle', familia_id=familia_id  )
    else:
        logger.debug("CAMINO 2 Plan de Pago NUEVO {}".format(plan_pagos_id))

        form = PlanDePagoForm(instance=plan_de_pago)
        form.fields['nombre'].disabled = True
        form.fields['descripcion'].disabled = True
        form.fields['crm_id'].disabled = True
        #logger.debug("From:{}".format(form))
    
    op_title='Nuevo Plan de pago a famlia {}'.format(familia.familia_crm_id)
    boton_aceptar='Agregar Plan de pago'
    boton_cancelar='Descartar nuevo Plan de pago'

    logger.debug("Plan de Pago nuevo END")
    return render(request, 'cuotas/nuevo_cuotas_plan.html', {'form': form, 'plan_de_pago':plan_de_pago, 'familia': familia, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })
    # return render(request, 'socios/familia_nuevo.html', {'form': form, "familia": familia_socios, 'boton_aceptar': boton_aceptar, 'boton_cancelar': boton_cancelar, 'op_title': op_title })

def editar_cuota(request, familia_id, cuota_id):

    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.info(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    cuota = CuotaSocialFamilia.objects.get(pk=cuota_id)
    logger.info("{}) Cuota {} Familia {} plan de pagos {} ".format(func.co_name,cuota.pk,cuota.familia.familia_crm_id,cuota))

    if request.method == "POST":
        form = CuotaSocialFamiliaForm(request.POST,instance=cuota)
        # check whether it's valid:
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('socios:familia_detalle', familia_id=familia_id  )

    
    form = CuotaSocialFamiliaForm(instance=cuota)

    return render(request, 'cuotas/cuota_editar.html', {'form': form, 'cuota': cuota })

def borrar_cuota(request, familia_id, cuota_id):

    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.info(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
 # GENERAR DELETE DE CUOTA - esto copia el editar_cuota
    cuota = CuotaSocialFamilia.objects.get(pk=cuota_id)
    logger.info("FORM DELETE CUOTA {}) Cuota {} Familia {} plan de pagos {} ".format(func.co_name,cuota.pk,cuota.familia.familia_crm_id,cuota))

    if request.method == "POST" and 'delete' in request.POST:
        form = CuotaSocialFamiliaForm(instance=cuota)
        #logger.info("FORM DELETE CUOTA POST {}) Cuota {} Familia {} plan de pagos {} valid {} ".format(func.co_name,cuota.pk,cuota.familia.familia_crm_id,cuota,form.is_valid()))
        # check whether it's valid:
        #if form.is_valid():
        form.is_valid()
        post = form.save(commit=False)
        post.deleted = True
        post.save()
        logger.info("FORM POST {} IS VALID".format(form))
        return redirect('socios:familia_detalle', familia_id=familia_id  )
        #else:
        #    logger.info("FORM DELETE INVALID CUOTA POST {}) Cuota {} Familia {} plan de pagos {} errores {} ".format(func.co_name,cuota.pk,cuota.familia.familia_crm_id,cuota,form.errors))

    
    form = CuotaSocialFamiliaForm(instance=cuota)
    form.fields['vencimiento'].widget.attrs['disabled'] = 'disabled'
    form.fields['importe_cuota'].widget.attrs['disabled'] = 'disabled'
    form.fields['plan_de_pago'].widget.attrs['disabled'] = 'disabled'
    form.fields['familia'].widget.attrs['disabled'] = 'disabled'
    
    #logger.info(" RENDER {}) Cuota {} Familia {} plan de pagos {} ".format(func.co_name,cuota.pk,cuota.familia.familia_crm_id,cuota))
    return render(request, 'cuotas/cuota_borrar.html', {'form': form, 'cuota': cuota })



