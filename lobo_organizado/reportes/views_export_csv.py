from datetime import datetime
import os
from django.shortcuts import render
#from django.http import FileResponse
from django.http import HttpResponse
import csv
import inspect ,logging
from django.templatetags.static import static
from django.conf import settings
from socios.models import Familia
#from PIL import Image

logger = logging.getLogger('project.lobo.organizado')
# Create your views here.

def reporte_estado_de_cuenta_csv(current_user,data,filter_info):
    ''' prueba de listado familia, luego cambiar data por request y adaptar'''

    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("CSV DATA SOURCE: {} FILTERS: {}".format(data , filter_info) )
    
    headings = [
            "#",
            "CRM_ID",
            "Flia",
            "Plan",
            "vencido" ,
            "Cobrado" ,
            "Saldo Vdo",
            "Estado",
    ]
    
    count = 0

    #csv_report = reportes_csv(current_user,headings)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filter_info_String = []
    for item in filter_info:
      filter_info_String.append( item + '_' + str( filter_info[item]) ) 
    report_fullpath = "vl_reporte_cobranza_saldos.{}.{}.csv".format(timestamp, "__".join(filter_info_String))

    response = HttpResponse(
        content_type="text/csv",
       headers={"Content-Disposition": 'attachment; filename="{}"'.format(report_fullpath)},
    )
    output_csv= csv.writer(response)
    output_csv.writerow( headings)
    
    for row in data:
        #print(row.familia)
        count+=1
        output_csv.writerow( [
            str(count),
            row.familia.crm_id,
            row.familia.familia_crm_id,
            row.plan_de_pago,
            row.cuotas_vencidas_importe,
            row.pagos_importe,
            row.balance,'OK' if row.balance <= 0 else 'DEUDA'
            ] )
    
    return response


def reporte_estado_familias_csv(current_user,data,filter_info):
    ''' prueba de listado familia, luego cambiar data por request y adaptar'''

    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("PDF DATA SOURCE: {} FILTERS: {}".format(data , filter_info) )
    
    headings = (
            "#",
            "ID",
            "Familia",
            "Modificado"
        )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%s")
 
    report_fullpath = os.path.join(settings.DATA_PDF_PATH,"vl_reporte_saldos.{}.csv".format(timestamp))

    response = HttpResponse(
        content_type="text/csv",
       headers={"Content-Disposition": 'attachment; filename="{}"'.format(report_name)},
    )
    output_csv= csv.writer(response)
    output_csv.writerow( headings)
    count = 0
    for row in data:
        #logger.debug(row.crm_id)
        count+=1
        pdf.cell(col_widths[0], cell_v, str(count), "LR", 0, "L", fill)
        logger.debug("{}-{}".format(row.crm_id,row.familia_crm_id) )
        pdf.cell(col_widths[1], cell_v, str(row.crm_id) , "LR", 0, "L", fill)
        pdf.cell(col_widths[2], cell_v, str(row.familia_crm_id), "LR", 0, "L", fill)
        pdf.cell(col_widths[3], cell_v, str(row.actualizado), "LR", 0, "L", fill)
        output_csv.writerow( [
            str(count),
            str(row.crm_id),
            str(row.familia_crm_id),
            str(row.actualizado)
            ] )
    
    return response


def reporte_cobranza_csv(current_user,data,filter_info):
    '''Reporte de pago de cuotas percibidos'''

    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("CSV DATA SOURCE: {} FILTERS: {}".format(data , filter_info) )
    
    headings = (
            "#",
            "ID",
            "Familia",
            "Fecha",
            "Plan",
            "$$$",
            'M#',
            "Comprobante"
        )
    

    count = 0

    #csv_report = reportes_csv(current_user,headings)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filter_info_String = []
    for item in filter_info:
      filter_info_String.append( item + '_' + str( filter_info[item]) ) 
    report_fullpath = "vl_reporte_cobranza.{}.{}.csv".format(timestamp, "__".join(filter_info_String))

    response = HttpResponse(
        content_type="text/csv",
       headers={"Content-Disposition": 'attachment; filename="{}"'.format(report_fullpath)},
    )
    output_csv= csv.writer(response)
    output_csv.writerow( headings)
    
    for row in data:
        #print(row.familia)
        count+=1
        if row.comprobante:
            comprobante = f'{row.comprobante} / {row.hash}'
        else:
            comprobante = f'{row.hash}'
        output_csv.writerow( [
            str(count),
            str(row.familia.crm_id),
            row.familia.familia_crm_id,
            row.fecha_cobro,
            row.aplica_pago_plan.crm_id,
            row.importe,
            row.forma_de_pago.medio_id,
            comprobante
            ] )
            
    
    return response



def index_csv(request):

    return None


def socios_familia_csv(familias):

    # continuas TODO 
    return None
