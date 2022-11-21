#
import inspect ,logging
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
from reportes.views import reporte_estado_de_cuenta,reporte_cobranza
from decimal import Decimal
import cuotas.models as app_cuotas

#from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse
from socios.models import Familia
from cuotas.models import PlanDePago,CuotaPago,CuotaSocialFamilia,CuotaMedioDePago
from auditlog.models import LogEntry


logger = logging.getLogger('project.lobo.organizado')

def auditoria_cobranza_cuota_familia(request, familia_id):
    '''Auditoria de pagos de una familia'''

    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.info(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    error_message = ''
    page_obj = None

    selected_family = Familia.objects.get(pk=familia_id)
    objs = app_cuotas.pagos_percibidos_queryset(familia_id)

    log = Familia.objects.first().history.latest() 
    audit_changes = selected_family,log.changes_display_dict
    chagelist = log.changes_dict
    logger.debug("## Familia {} ) history {} ".format(func.co_name,audit_changes[1]))

    print(Familia.objects.first().history.latest().changes_dict)
    print("================")
    for k in chagelist:
        print(k)
        logger.debug("REC {} : {} > {} - {} - {} ".format(func.co_name, k ,chagelist[k] ,chagelist[k][0],chagelist[k][1] ) )
    logger.debug("======================================")

    for i in objs:
        logger.debug("Familia {} ) Cuota {} - {} {} -".format(func.co_name,selected_family,i.fecha_cobro, i.importe))

    logger.debug("Familia {} ) Cuotas {} ".format(func.co_name,selected_family,len( [  x  for x in objs  ] ) ))

    # objs = CuotaSocialFamilia.objects.all()
    # objs = CuotaPago.objects.first()
    #rel_history = LogEntry.objects.get_for_objects(objs.related.all())
    full_history = (objs[1].history.all() ).order_by('-timestamp')

    return render(request, 'cuotas/auditory_cobranza_cuota_familia.html', {
        'error_message': error_message,
        'full_history' : full_history,
        'mymodel' : chagelist.items
        } )