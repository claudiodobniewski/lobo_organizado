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

class SaldosFamilia():

    CUOTA='c'
    PAGO='p'

    def __init__(self,q_cuotas,q_pagos,planes_de_pago):

        #cuotas = None
        #pagos = None 
        self.registros = []
        self.saldo = 0.0
        
        self.cuotas = list( q_cuotas.order_by('vencimiento') )
        self.pagos = list( q_pagos.order_by('fecha_cobro') )

        self.planes_de_pago = planes_de_pago
        print("cuotas cantidad:{}  pagos cantidad:{}".format( len(self.cuotas),len(self.pagos) ))
    
    def proceso_corto(self):
        ''' proceso corto si cuotas o pagos esta vacia
            @return True si no requiere proceso adicional.
        '''

        if not len(self.cuotas) and not len(self.pagos):
            print("* No hay cuotas ni pagos! C:{} P:{}".format(len(self.cuotas) ,len(self.pagos)) )
            return True
        elif not len(self.pagos) :
            print("* aplica_solo_cuotas()")
            self.aplica_solo_cuotas()
            return True

        elif not len(self.cuotas) :
            print("* aplica_solo_pagos()")
            self.aplica_solo_pagos()
            return True

        return False

    def aplica_solo_pagos(self):

        while len(self.pagos) :
            pago=self.pagos.pop(0)
            self.registros.append(self.aplica_un_pago(pago))
    
    def aplica_un_pago(self,pago):
        
        self.saldo += float ( pago.importe )
        reg = {
            "fecha": pago.fecha_cobro , 
            "cuota": 0.0,
            "pago" : float ( pago.importe ),
            "saldo" : self.saldo,
            "tipo": self.PAGO,
            "plan": self.planes_de_pago.filter(pk=pago.aplica_pago_plan.id)[0].crm_id
        }
        return reg


    def aplica_solo_cuotas(self):

        while len(self.cuotas) > 0 :
            print("Aplicando cuota...")
            cuota=self.cuotas.pop(0)
            self.registros.append(self.aplica_una_cuota(cuota))

    def aplica_una_cuota(self,cuota):

        self.saldo -= cuota.importe_cuota
        reg = {
            "fecha": cuota.vencimiento , 
            "cuota": cuota.importe_cuota ,
            "pago" : 0.0 ,
            "saldo" : self.saldo,
            "tipo": self.CUOTA,
            "plan": self.planes_de_pago.filter(pk=cuota.plan_de_pago.id)[0].crm_id
        }
        return reg

    def aplica_cuota_mas_vieja(self,cuota,pago):
        ''' '''
        print("older vencimiento < cobro ? {} ".format(cuota.vencimiento < pago.fecha_cobro))
        if cuota.vencimiento < pago.fecha_cobro:
            print("aplicando Cuota...")
            self.registros.append(self.aplica_una_cuota(cuota))
            cuota = None
        else:
            print("aplicando Pago...")
            self.registros.append(self.aplica_un_pago(pago))
            pago = None
        return (cuota,pago)

    def procesar(self):

        # si hay cutoas y pagos...

        if self.proceso_corto():
            print("Return en proceso_corto() inicial")
            return 
        
        #first_loop = True
        c=None
        p=None
        print("Start loop")
        while len(self.cuotas) or len(self.pagos) or not c or not p:
            print("Nest loop....")
            #if first_loop:
            #    print("Firts loop!")
            #    c = self.cuotas.pop()
            #    p = self.pagos.pop()

            if not c and len(self.cuotas):
                c = self.cuotas.pop(0)
                print("C.pop({})".format(c))
            elif not c and not len(self.cuotas):
                if p :
                    self.pagos.insert(0,p)
                print("C no tiene mas elementos, break loop")
                break
            
            if not p and len(self.pagos) :
                p = self.pagos.pop(0)
                print("P.pop({})".format(p))
            elif not p  and not len(self.pagos) :
                if c:
                    self.cuotas.insert(0,c)
                print("P no tiene mas elementos, break loop")
                break
            
            print("* cuotas:{}  pagos:{}".format( len(self.cuotas),len(self.pagos) ))
            print("* cuota:{}  pagos:{}".format( c,p ))

            c,p = self.aplica_cuota_mas_vieja(c,p)
            print("* post aplicar c,p :: {} ## {}".format(c,p))
            print("* Registros: {}".format(self.registros))
            print("CHECK LOOP CONDITION: lenC:{}, lenP{}, NOT c:{} , NOT p:{}, BOOLEAN:{}".format(len(self.cuotas) , len(self.pagos) , not c , not p,len(self.cuotas) or len(self.pagos) or not c or not p))
            print("end loop")
            
            

        # finalmente, o no hay mas cuotas o no hay mas pagos...
        result_corto = self.proceso_corto()
        print("** result:{} Registros: {}".format(result_corto,self.registros))
        print("end procesar()")

    def get_registros(self):
        return self.registros


    

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
    f_familia = None
    lista_cuotas = CuotaSocialFamilia.objects.all().filter(deleted=False)
    

     # BUSQUEDA
     
    if not clean_filters and request.method == 'GET': # If the form is submitted
        print("GET :{}".format(request.GET) )
        f_start_date=request.GET.get('f_start_date', None)
        f_end_date=request.GET.get('f_end_date', None)
        f_plan=request.GET.get('f_plan', None)
        f_familia = request.GET.get('f_familia', None)
        
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
    print("GET:{} POST:{} FAMILIA:{} PLAN:{}  CUOTAS:{}".format(request.GET.get('f_start_date', None),request.POST.get('f_start_date', None),request.POST.get('f_familia', None),f_plan,lista_cuotas ))
    

    ###############################
    # BUSQUEDA
    

    if f_familia:
        lista_familias = Familia.objects.filter(familia_crm_id__icontains=f_familia).filter(eliminado=False).order_by('familia_crm_id')
    else:
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
        
       
        if plan:
            print("Entro en plan filtro="+plan)
            estado_plan = EstadoPlan()
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
                estado_plan = EstadoPlan()
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

        #####
        # Paginacion
        paginator = Paginator(reporte, 15) # Show x contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, 'cuotas/g_cobranzas_listado.html', {
        'error_message': error_message,
        'page_obj': page_obj,
        'f_start_date': f_start_date,
        'f_end_date': f_end_date,
        'f_plan': f_plan,
        'f_familia': f_familia
         } )

def gestion_cobranza_familia(request, familia_id):
    '''detalla cuotas y pagos de la familia, con saldo por movimiento'''

    familia = Familia.objects.get(pk=familia_id,eliminado=False)
    cuotas = app_cuotas.cuotas_queryset(familia.id)
    pagos = app_cuotas.pagos_percibidos_queryset(familia.id)
    planes_de_pago =  PlanDePago.objects.all().order_by('id')
    registros=[]
    
    for plan in planes_de_pago:
        print("planes de pago...gestion cobranza")
        cuotas_plan = app_cuotas.cuotas_por_plan(cuotas,plan.id)
        pagos_plan = app_cuotas.pagos_percibidos_plan(pagos,plan.id)
        print("Cuotas: {}".format(cuotas_plan))
        print("Pagos: {}".format(pagos_plan))
        gestion = SaldosFamilia(cuotas_plan,pagos_plan,planes_de_pago)
        gestion.procesar()
        registros = gestion.get_registros()
        del gestion

    print("REGISTROS: {}".format(registros))
    for i in registros:
        print("Item: {}".format(i))
        print("fecha:{} cuota:{} pago:{} saldo:{}".format(i['fecha'],i['cuota'],i['pago'],i['saldo'
        ]))
    
    return render(request, 'cuotas/g_cobranzas_familia.html', {
        #'error_message': '',
        #'page_obj': page_obj,
        #'f_start_date': f_start_date,
        #'f_end_date': f_end_date,
        #'f_plan': f_plan
        'familia': familia,
        'registros': registros
         } )
        





