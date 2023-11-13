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
 
    report_fullpath = os.path.join(settings.DATA_PDF_PATH,"vl_reporte_cobranza_saldos.{}.csv".format(timestamp))

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
    full_width =  sum (len(x) for x in headings )
    page_width = 270
    col_widths = [  int((len(x)/full_width)*page_width)  for x in headings ]
    col_widths = [7,15,50,30,25,23,10,110]
    logger.debug("PDF WIDTH FULL : {} WEIGHTS: {}".format(full_width , col_widths) )
    
    count = 0
    #model_fields = [f.name for f in data._meta.get_fields()]
    #rows = [ r[0] for r in data if model_fields in field_names ]

    pdf = reportes_pdf('L', 'mm', 'A4',current_user)
    report_fullpath = os.path.join(settings.DATA_PDF_PATH,"vl_reporte_cobranza_saldos.{}.pdf".format(pdf.timestamp))
    pdf.set_title( "Viejos Lobos - reporte Cuotas Cobradas" )
    pdf.alias_nb_pages()
    pdf.set_image_filter("DCTDecode")
    pdf.add_page()
    pdf.set_font("Courier", size=10)
    #pdf.write(6,"Usuario:{}-{},{} Fecha Reporte {}".format(pdf.current_user.pdf.id,current_user.last_name, pdf.current_user.first_name,pdf.timestamp))
    #pdf.ln()
    #pdf.basic_table(headers,field_names, data)
    #pdf.colored_table(headers,field_names, data)
    
    pdf.write(6,"Filtros aplicados {}".format(str(filter_info)))
    pdf.ln()
    pdf.set_fill_color(255, 100, 0)
    pdf.set_text_color(255)
    pdf.set_draw_color(255, 0, 0)
    pdf.set_line_width(0.3)
    pdf.set_font(style="B")
    for col_width, heading in zip(col_widths, headings):
        pdf.cell(col_width, 5, heading, 1, 0, "C", True)
    pdf.ln()
    # Color and font restoration:
    pdf.set_fill_color(224, 235, 255)
    pdf.set_text_color(0)
    pdf.set_font()
    fill = False

    for row in data:
        #logger.debug(row.hash)
        count+=1
        cell_v=5
        pdf.cell(col_widths[0], cell_v, str(count), "LR", 0, "L", fill)
        #logger.debug("{}-{}".format(row.id,row.familia.familia_crm_id) )
        pdf.cell(col_widths[1], cell_v, str(row.id) , "LR", 0, "L", fill)
        pdf.cell(col_widths[2], cell_v, str(f"{row.familia.crm_id}#{row.familia.familia_crm_id}") , "LR", 0, "L", fill)
        pdf.cell(col_widths[3], cell_v, str(row.fecha_cobro) , "LR", 0, "L", fill)
        pdf.cell(col_widths[4], cell_v, str(row.aplica_pago_plan.crm_id), "LR", 0, "L", fill)
        pdf.cell(col_widths[5], cell_v, str(row.importe), "LR", 0, "L", fill)
        pdf.cell(col_widths[6], cell_v, str(row.forma_de_pago.medio_id), "LR", 0, "L", fill)
        if row.comprobante:
            comprobante = f'{row.comprobante} / {row.hash}'
        else:
            comprobante = f'{row.hash}'
        pdf.cell(col_widths[7], cell_v,comprobante, "LR", 0, "L", fill)
        
        pdf.ln()
        fill = not fill
    pdf.cell(page_width, 0, "", "T")
    pdf.output(  report_fullpath)
    return FileResponse(open(report_fullpath, 'rb'), as_attachment=True, content_type='application/pdf')



def index_csv(request):

    return None


def socios_familia_csv(familias):

    # continuas TODO 
    return None
