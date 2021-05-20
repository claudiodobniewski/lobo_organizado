#
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect
#from datetime import datetime,timedelta
import datetime
from django.core.paginator import Paginator
from .forms import CuotaPagoForm, CuotaSocialFamiliaForm, PlanDePagoForm
from socios.models import Familia
from cuotas.models import PlanDePago,CuotaPago,CuotaSocialFamilia
from decimal import Decimal




def gestion_cobranza_listado(request, error_message=''):

    f_start_date = None
    f_end_date = None
    f_plan = None
     # BUSQUEDA
    if request.method == 'GET': # If the form is submitted
        f_start_date = request.GET.get('f_start_date', None)
        f_end_date = request.GET.get('f_end_date', None)
        f_plan = request.GET.get('f_plan', None)
    else:
        f_start_date = None
        f_end_date = None
        f_plan = None

    if not f_start_date:
        f_start_date = datetime.date.today() # - timedelta(months = 1)
    else:
        f_start_date = datetime.date(f_start_date)

    if not f_end_date:
        f_end_date = datetime.date.today()
    else:
        f_end_date = datetime.date(f_end_date)
    print("START_DATE:{} END_DATE:{}".format(f_start_date,f_end_date) )
    lista_cuotas = CuotaSocialFamilia.objects.all()
    lista_cuotas = lista_cuotas.filter(deleted=False)
    #lista_cuotas = lista_cuotas.filter(vencimiento__gte=f_start_date)
    #lista_cuotas = lista_cuotas.filter(vencimiento__lte=f_end_date)
    lista_cuotas = lista_cuotas.order_by('vencimiento')
    
    if f_plan:
        lista_cuotas = lista_cuotas.objects.filter(plan_de_pago=f_plan)

    print("GET:{} POST:{}  PLAN:{}  CUOTAS:{}".format(request.GET.get('f_start_date', None),request.POST.get('f_start_date', None),f_plan,lista_cuotas ))
    
     # Paginacion
    paginator = Paginator(lista_cuotas, 8) # Show x contacts per page.
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


