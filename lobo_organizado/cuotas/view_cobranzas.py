#
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect
from django.template.defaulttags import register
import datetime
from datetime import datetime,date #,timedelta
from django.core.paginator import Paginator
from .forms import CuotaPagoForm, CuotaSocialFamiliaForm, PlanDePagoForm
from socios.models import Familia
from cuotas.models import PlanDePago,CuotaPago,CuotaSocialFamilia
from decimal import Decimal
import cuotas.models as app_cuotas


class EstadoPlan():

    familia = None
    plan_de_pago = None
    cuotas = None
    cuotas_vencidas = None
    cuotas_vencidas_importe = None
    pagos = None
    pagos_importe = None
    balance = None
    estado = None

@register.filter(name='absolute')
def absolute(value):
    """Removes all values of arg from the given string"""
    if value:
        return abs(value)
    else:
        return 0.0

def gestion_cobranza_listado(request, clean_filters=False, error_message=''):

    start_date = None
    end_date = None
    plan = None
    lista_cuotas = CuotaSocialFamilia.objects.all().filter(deleted=False)
    

     # BUSQUEDA
     
    if not clean_filters and request.method == 'GET': # If the form is submitted
        print("GET :{}".format(request.GET) )
        f_start_date=request.GET.get('f_start_date', None)
        f_end_date=request.GET.get('f_end_date', None)
        f_plan=request.GET.get('f_plan', None)
        
        if not f_start_date:
            start_date = date.today() # - timedelta(months = 1)
        else:
            start_date = datetime.date(datetime.strptime(f_start_date,"%Y-%m-%d"))
            lista_cuotas = lista_cuotas.filter(vencimiento__gte=start_date)

        if not f_end_date:
            end_date = date.today()
        else:
            end_date = datetime.date(datetime.strptime(f_end_date,"%Y-%m-%d"))
        lista_cuotas = lista_cuotas.filter(vencimiento__lte=end_date)
        
        plan = f_plan
        if plan:
            lista_cuotas = lista_cuotas.filter(plan_de_pago=plan)
    else:
        print("NO FILTERS {}: {}".format(clean_filters,request.GET) )
        f_start_date=''
        f_end_date = date.today().strftime("%Y-%m-%d")
        end_date = date.today()
        f_plan=None
    
    print(date.today())
    print("GET:{} POST:{}  PLAN:{}  CUOTAS:{}".format(request.GET.get('f_start_date', None),request.POST.get('f_start_date', None),f_plan,lista_cuotas ))
    

    ###############################
    lista_familias = Familia.objects.all().filter(eliminado=False).order_by('familia_crm_id')
    
    if plan:
        lista_planes = PlanDePago.objects.get(id=plan)
    else:
        lista_planes = PlanDePago.objects.all().order_by('id')
    
    reporte = []
    
    print(" FECHA DESDE:{} HASTA:{} PLAN:{} PLANES:{}".format(start_date,end_date,plan,lista_planes))
    for familia in lista_familias:

        # cuotas_todas,cuotas_por_plan,cuotas_vencidas,cuotas_suma,pagos_percibidos_queryset,pagos_percibidos_plan,pagos_percibidos_suma
        ## TODO ver paginado si dejamos una pagina o N registros
        ## TODO ver familias que no tienen deuda (un filtro mas, o paginas distintas?)
        ## analizar el "start_date" si lo aplicamos
        ## TODO default value para end_date today en el filtro.

        cuotas = app_cuotas.cuotas_queryset(familia.id)
        pagos =  app_cuotas.pagos_percibidos_queryset(familia.id)
        estado_plan = EstadoPlan()
       
        if plan:
            print("Entro en 1 plan")
            estado_plan.familia = familia
            estado_plan.plan_de_pago = lista_planes
            estado_plan.cuotas = app_cuotas.cuotas_por_plan(cuotas,lista_planes)
            estado_plan.cuotas_vencidas = app_cuotas.cuotas_vencidas(cuotas,end_date)
            vencidas_importe = estado_plan.cuotas_vencidas_importe = app_cuotas.cuotas_suma(estado_plan.cuotas_vencidas)
            estado_plan.pagos = app_cuotas.pagos_percibidos_plan(pagos, lista_planes.id)
            print(estado_plan.pagos )
            pagos_importe = estado_plan.pagos_importe = app_cuotas.pagos_percibidos_suma(estado_plan.pagos)
            balance_plan =  estado_plan.balance = vencidas_importe - float (pagos_importe)
            estado_del_plan =  estado_plan.estado = 'OK' if balance_plan <= 0 else 'DEUDA'
            print("FLIA:{} ESTADOD EL PLAN [{}] VDO:{} COB:{} BAL:{} EST:{}".format(familia,lista_planes,vencidas_importe,pagos_importe,balance_plan,estado_del_plan))
            reporte.append(estado_plan)
            
        else:
            print("Entro en varios planes")
            for un_plan in lista_planes:
                estado_plan.familia = familia
                estado_plan.plan_de_pago = app_cuotas.cuotas_por_plan(cuotas,un_plan)
                estado_plan.plan_de_pago = un_plan
                estado_plan.cuotas = app_cuotas.cuotas_por_plan(cuotas,un_plan)
                estado_plan.cuotas_vencidas = app_cuotas.cuotas_vencidas(cuotas,end_date)
                vencidas_importe = estado_plan.cuotas_vencidas_importe = app_cuotas.cuotas_suma(estado_plan.cuotas_vencidas)
                estado_plan.pagos = app_cuotas.pagos_percibidos_plan(pagos, un_plan.id)
                print(estado_plan.pagos )
                pagos_importe = estado_plan.pagos_importe = app_cuotas.pagos_percibidos_suma(estado_plan.pagos)
                balance_plan =  estado_plan.balance = vencidas_importe - float (pagos_importe)
                estado_del_plan =  estado_plan.estado = 'OK' if balance_plan <= 0 else 'DEUDA'
                print("FLIA:{} ESTADOD EL PLAN [{}] VDO:{} COB:{} BAL:{} EST:{}".format(familia,un_plan,vencidas_importe,pagos_importe,balance_plan,estado_del_plan))
                reporte.append(estado_plan)
            reporte.append(estado_plan)

        #####
        # Paginacion
        paginator = Paginator(reporte, 100) # Show x contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, 'cuotas/g_cobranzas_listado.html', {
        'error_message': error_message,
        'page_obj': page_obj,
        'f_start_date': f_start_date,
        'f_end_date': f_end_date,
        'f_plan': f_plan
         } )


