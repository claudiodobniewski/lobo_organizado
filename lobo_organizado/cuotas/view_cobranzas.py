#
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect
from django.template.defaulttags import register
import datetime
from datetime import datetime,date, timezone #,timedelta
from django.core.paginator import Paginator
from .forms import CuotaPagoForm, CuotaSocialFamiliaForm, PlanDePagoForm
from socios.models import Familia
from cuotas.models import PlanDePago,CuotaPago,CuotaSocialFamilia
from decimal import Decimal
import cuotas.models as app_cuotas

from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse




class EstadoPlan():

    def __init__(self):
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
            "comprobante": pago.comprobante,
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

@register.filter(name='eq_id')
def equal_id(plan_id,plan_option_id):
    """Evalua si ambos integers son iguales
    @param plan_id integer
    @param plan_option_iw integer    
    """
    print("PLAN_ID:{}  PLAN_OPTION_ID:{}  EQUALL:{}".format(plan_id,plan_option_id,int(plan_id) == int(plan_option_id) ) )
    return int(plan_id) == int(plan_option_id)

def gestion_cobranza_listado(request, clean_filters=False, error_message=''):

    start_date = None
    end_date = None
    f_plan = None
    f_familia = None
    lista_cuotas = CuotaSocialFamilia.objects.all().filter(deleted=False)
    #lista_planes = PlanDePago.objects.all().filter(eliminado=False)

     # BUSQUEDA
     
    if not clean_filters and request.method == 'GET': # If the form is submitted
        print("GET :{}".format(request.GET) )
        f_start_date=request.GET.get('f_start_date', None)
        f_end_date=request.GET.get('f_end_date', None)
        f_plan=int(request.GET.get('planes_de_pagos', None))
        #print("VERIFICANDO VALOR F_PLAN - GET:{}  VAR:{}".format(request.GET.get('planes_de_pagos', None),f_plan))
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
        
        #plan = f_plan
        if f_plan:
            lista_cuotas = lista_cuotas.filter(plan_de_pago=f_plan)




    else:
        print("NO FILTERS {}: {}".format(clean_filters,request.GET) )
        f_start_date=''
        f_end_date = date.today().strftime("%Y-%m-%d")
        end_date = date.today()
        f_plan=0
    
    print(date.today())
    print("GET:{} POST:{} FAMILIA:{} PLAN:{}  CUOTAS:{}".format(request.GET.get('f_start_date', None),request.POST.get('f_start_date', None),request.POST.get('f_familia', None),f_plan,lista_cuotas ))
    

    ###############################
    # BUSQUEDA
    

    if f_familia:
        lista_familias = Familia.objects.filter(familia_crm_id__icontains=f_familia).filter(eliminado=False).order_by('familia_crm_id')
    else:
        lista_familias = Familia.objects.all().filter(eliminado=False).order_by('familia_crm_id')
    
    lista_planes_view = PlanDePago.objects.all().order_by('id')

    if f_plan:
        print(" checkpint planes filtrado '{}' ".format(f_plan))
        lista_planes = PlanDePago.objects.all().filter(id=f_plan)
    else:
        lista_planes = lista_planes_view.all()
    
    #lista_planes = PlanDePago.objects.all().order_by('id')

    reporte = []
    
    print(" FECHA DESDE:{} HASTA:{} PLAN:{} PLANES:{}".format(start_date,end_date,f_plan,lista_planes))
    for familia in lista_familias:

        # cuotas_todas,cuotas_por_plan,cuotas_vencidas,cuotas_suma,pagos_percibidos_queryset,pagos_percibidos_plan,pagos_percibidos_suma
        ## TODO ver paginado si dejamos una pagina o N registros
        ## TODO ver familias que no tienen deuda (un filtro mas, o paginas distintas?)
        ## analizar el "start_date" si lo aplicamos
        ## TODO default value para end_date today en el filtro.

        cuotas = app_cuotas.cuotas_queryset(familia.id)
        pagos =  app_cuotas.pagos_percibidos_queryset(familia.id)

        for un_plan in lista_planes:
            estado_plan = EstadoPlan()
            estado_plan.familia = familia
            estado_plan.plan_de_pago = un_plan
            estado_plan.cuotas = app_cuotas.cuotas_por_plan(cuotas,un_plan)
            estado_plan.cuotas_vencidas = app_cuotas.cuotas_vencidas(estado_plan.cuotas,end_date)
            vencidas_importe = estado_plan.cuotas_vencidas_importe = app_cuotas.cuotas_suma(estado_plan.cuotas_vencidas)
            estado_plan.pagos = app_cuotas.pagos_percibidos_plan(pagos, un_plan.id)
            if not len( estado_plan.cuotas ) and not len( estado_plan.pagos ):
                continue
            print("PLAN:: {}".format(un_plan) )
            pagos_importe = estado_plan.pagos_importe = app_cuotas.pagos_percibidos_suma(estado_plan.pagos)
            balance_plan =  estado_plan.balance = vencidas_importe - float (pagos_importe)
            estado_del_plan =  estado_plan.estado = 'OK' if balance_plan <= 0 else 'DEUDA'
            print("FLIA:{} ++ ESTADO DEL PLAN [{}] VDO:{} COB:{} BAL:{} EST:{}".format(familia,un_plan,vencidas_importe,pagos_importe,balance_plan,estado_del_plan))
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
        'f_familia': f_familia,
        'lista_planes': lista_planes_view
         } )

def gestion_cobranza_familia(request, familia_id):
    '''detalla cuotas y pagos de la familia, con saldo por movimiento'''

    familia = Familia.objects.get(pk=familia_id,eliminado=False)
    cuotas = app_cuotas.cuotas_queryset(familia.id).filter(deleted=False).order_by('vencimiento')
    pagos = app_cuotas.pagos_percibidos_queryset(familia.id).filter(deleted=False).order_by('fecha_cobro')
    planes_de_pago =  PlanDePago.objects.all().order_by('id')
    registros=[]
    
    gestion = SaldosFamilia(cuotas,pagos,planes_de_pago)
    gestion.procesar()
    registros.extend(gestion.get_registros())

    print("REGISTROS: {}".format(registros))
    for i in registros:
        print("Item: {}".format(i))
        print("fecha:{} cuota:{} pago:{} saldo:{}".format(i['fecha'],i['cuota'],i['pago'],i['saldo']))
    
    #print("IMPRESION PDF" )
    #pdf_generation(request)

    return render(request, 'cuotas/g_cobranzas_familia.html', {
        #'error_message': '',
        #'page_obj': page_obj,
        #'f_start_date': f_start_date,
        #'f_end_date': f_end_date,
        #'f_plan': f_plan
        'familia': familia,
        'registros': registros
         } )

def gestion_pagos_listado(request, clean_filters=False, error_message=''):

    start_date = None
    end_date = None
    f_plan = None
    f_familia = None
    lista_pagos = CuotaPago.objects.all().filter(deleted=False).order_by('-fecha_cobro')

    # BUSQUEDA
    
    

    if not clean_filters and request.method == 'GET': # If the form is submitted
        print("GET :{}".format(request.GET) )
        f_start_date=request.GET.get('f_start_date', None)
        f_end_date=request.GET.get('f_end_date', None)
        f_plan=int(request.GET.get('planes_de_pagos', None))
        #print("VERIFICANDO VALOR F_PLAN - GET:{}  VAR:{}".format(request.GET.get('planes_de_pagos', None),f_plan))
        f_familia = request.GET.get('f_familia', None)
        
        if not f_start_date:
            start_date = date.today() # - timedelta(months = 1)
        else:
            start_date = datetime.date(datetime.strptime(f_start_date,"%Y-%m-%d"))
            lista_pagos = lista_pagos.filter(fecha_cobro__gte=start_date)

        if not f_end_date:
            end_date = date.today()
        else:
            end_date = datetime.date(datetime.strptime(f_end_date,"%Y-%m-%d"))
        lista_pagos = lista_pagos.filter(fecha_cobro__lte=end_date)
        print("Pagos 1 {}".format(lista_pagos))
        
        if f_plan:
            lista_pagos = lista_pagos.filter(aplica_pago_plan=f_plan)
            print("Pagos 2 {}  {}".format(f_plan,lista_pagos))

        
        if f_familia:
            lista_familias = Familia.objects.filter(familia_crm_id__icontains=f_familia).filter(eliminado=False).order_by('familia_crm_id')
            print("Familias {}".format(lista_familias))
            print("Pagos 3 {}".format(lista_pagos))
            lista_pagos = lista_pagos.filter(deleted=False).filter(familia__pk__in=lista_familias)
            lista_pagos = CuotaPago.objects.all().filter(deleted=False).filter(familia__pk__in=lista_familias).order_by('-fecha_cobro')

            print("Pagos 4 {}".format(lista_pagos))
            
        #else:
        #    lista_familias = Familia.objects.all().filter(eliminado=False).order_by('familia_crm_id')

    else:
        print("NO FILTERS {}: {}".format(clean_filters,request.GET) )
        f_start_date=''
        f_end_date = date.today().strftime("%Y-%m-%d")
        end_date = date.today()
        f_plan=0

    lista_planes_view = PlanDePago.objects.all().order_by('id')
    if f_plan:
        print(" checkpint planes filtrado '{}' ".format(f_plan))
        lista_planes = PlanDePago.objects.all().filter(id=f_plan)
    else:
        lista_planes = lista_planes_view.all()

    reporte = lista_pagos

    #####
    # Paginacion
    paginator = Paginator(reporte, 15) # Show x contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cuotas/g_pagos_listado.html', {
        'error_message': error_message,
        'page_obj': page_obj,
        'f_start_date': f_start_date,
        'f_end_date': f_end_date,
        'f_plan': f_plan,
        'f_familia': f_familia,
        'lista_planes': lista_planes_view
         } )

def pdf_generation(request):
            html_template = get_template('templates/home_page.html')
            pdf_file = HTML(string=html_template).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="home_page.pdf"'
            return response




