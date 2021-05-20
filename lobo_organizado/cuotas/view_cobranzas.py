#
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect
import datetime
from datetime import datetime,date #,timedelta
from django.core.paginator import Paginator
from .forms import CuotaPagoForm, CuotaSocialFamiliaForm, PlanDePagoForm
from socios.models import Familia
from cuotas.models import PlanDePago,CuotaPago,CuotaSocialFamilia
from decimal import Decimal




def gestion_cobranza_listado(request, error_message=''):

    start_date = None
    end_date = None
    plan = None
    lista_cuotas = CuotaSocialFamilia.objects.all().filter(deleted=False)


     # BUSQUEDA
     
    if request.method == 'GET': # If the form is submitted
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
        start_date = None
        end_date = None
        plan = None

    
    print("START_DATE:{} END_DATE:{}".format(start_date,end_date) )
    
    

    lista_cuotas = lista_cuotas.order_by('vencimiento')
    
    

    print("GET:{} POST:{}  PLAN:{}  CUOTAS:{}".format(request.GET.get('f_start_date', None),request.POST.get('f_start_date', None),f_plan,lista_cuotas ))
    
     # Paginacion
    paginator = Paginator(lista_cuotas, 100) # Show x contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cuotas/g_cobranzas_listado.html', {
        'cuotas': lista_cuotas, 
        'error_message': error_message,
        'page_obj': page_obj,
        'f_start_date': f_start_date,
        'f_end_date': f_end_date,
        'f_plan': f_plan
         } )


