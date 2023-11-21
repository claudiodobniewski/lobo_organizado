from datetime import datetime
import os
from django.shortcuts import render
from django.shortcuts import render
from django.http import FileResponse
from fpdf import FPDF
import inspect ,logging
from django.templatetags.static import static
from django.conf import settings
from socios.models import Familia,Socio
from reportes.views_export_csv import *

#from PIL import Image

logger = logging.getLogger('project.lobo.organizado')
# Create your views here.

class reportes_pdf(FPDF):

    def __init__(self,orientation = 'P', unit = 'mm', format='A4', current_user=None):

        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%s")
        self.current_user = current_user
        super().__init__(orientation , unit , format)
        self.use_footer=False

    def header(self):

        #self.allow_images_transparency = True
        logo_path = os.path.join(settings.STATIC_ROOT , 'institucional/logo_lobo_aullador_cortado.png')
        #img = Image.open(logo_path)
        #img = img.crop((10, 10, 490, 490)).resize((96, 96), resample=Image.NEAREST)
        # Rendering logo:
        self.image(logo_path, 10, 8, 20)
        # Setting font: helvetica bold 15
        self.set_font("Courier", "", 12)
        #self.set_stretching(100.0)
        # Moving cursor to the right:
        self.cell(30)
        # Printing title:
        width = self.get_string_width(self.title) + 6
        self.cell(width, 10, self.title, 1, 0, "C")
        # Performing a line break:
        self.ln(20)

    def footer(self):
        
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        if not self.use_footer:
            # Printing page number:
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}"+" Usuario:{}-{},{} Fecha Reporte {}".format(self.current_user.id,self.current_user.last_name, self.current_user.first_name,self.timestamp), 0, 0, "C")
        else:
            self.cell(0, 10, self.use_footer, 0, 0, "C")

    def basic_table(self, headings, rows, data):
        '''heading: encabezados - rows: nombres de campo en la columna - data: queryset de modelo con la informacion'''
        for heading in headings:
            self.cell(40, 6, heading, 1)
        self.ln()
        for reg in data:
            for row in rows:
                self.cell(40, 5, getattr(reg,row), 1)
            self.ln()

    def colored_table(self, headings, rows, data, col_widths=(42, 39, 35, 42)):
        '''heading: encabezados - rows: nombres de campo en la columna - data: queryset de modelo con la informacion'''
        # Colors, line width and bold font:
        self.set_fill_color(255, 100, 0)
        self.set_text_color(255)
        self.set_draw_color(255, 0, 0)
        self.set_line_width(0.3)
        self.set_font(style="B")
        for col_width, heading in zip(col_widths, headings):
            self.cell(col_width, 4, heading, 1, 0, "C", True)
        self.ln()
        # Color and font restoration:
        self.set_fill_color(224, 235, 255)
        self.set_text_color(0)
        self.set_font()
        fill = False
        for reg in data:
            for row in rows:
                logger.debug("PDF ROW: {} REG: {} DATA: {} ".format(row,reg,getattr(reg,row)) )
                self.cell(40, 4, getattr(reg,row), "LR", 0, "L", fill)
            self.ln()
            fill = not fill
        self.cell(120, 0, "", "T")

#### 

def reporte_estado_de_cuenta_pdf(current_user,data,filter_info):
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
            "CRM_ID",
            "Plan",
            "vencido" ,
            "Cobrado" ,
            "Saldo Vdo",
            "Estado",
        )
    full_width =  sum (len(x) for x in headings )
    page_width = 270
    col_widths = [  int((len(x)/full_width)*page_width)  for x in headings ]
    logger.debug("PDF WIDTH FULL : {} WEIGHTS: {}".format(full_width , col_widths) )
    
    count = 0
    #model_fields = [f.name for f in data._meta.get_fields()]
    #rows = [ r[0] for r in data if model_fields in field_names ]

    pdf = reportes_pdf('L', 'mm', 'A4',current_user)
    report_fullpath = os.path.join(settings.DATA_PDF_PATH,"vl_reporte_cobranza_saldos.{}.pdf".format(pdf.timestamp))
    pdf.set_title( "Viejos Lobos - reporte estados de cuenta SALDOS" )
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
        print(row.familia)
        count+=1
        cell_v=5
        pdf.cell(col_widths[0], cell_v, str(count), "LR", 0, "L", fill)
        logger.debug("{}-{}".format(row.familia.crm_id,row.familia.familia_crm_id) )
        pdf.cell(col_widths[1], cell_v, "{}-{}".format(row.familia.crm_id,row.familia.familia_crm_id), "LR", 0, "L", fill)
        pdf.cell(col_widths[2], cell_v, str(row.plan_de_pago), "LR", 0, "L", fill)
        pdf.cell(col_widths[3], cell_v, str(row.cuotas_vencidas_importe), "LR", 0, "L", fill)
        pdf.cell(col_widths[4], cell_v, str(row.pagos_importe), "LR", 0, "L", fill)
        pdf.cell(col_widths[5], cell_v, str(row.balance), "LR", 0, "L", fill)
        pdf.cell(col_widths[6], cell_v, 'OK' if row.balance <= 0 else 'DEUDA', "LR", 0, "L", fill)
        pdf.ln()
        fill = not fill
    pdf.cell(page_width, 0, "", "T")
    pdf.output(  report_fullpath)
    return FileResponse(open(report_fullpath, 'rb'), as_attachment=True, content_type='application/pdf')


def reporte_estado_familias(current_user,data,filter_info):
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
    full_width =  sum (len(x) for x in headings )
    page_width = 270
    col_widths = [  int((len(x)/full_width)*page_width)  for x in headings ]
    logger.debug("PDF WIDTH FULL : {} WEIGHTS: {}".format(full_width , col_widths) )
    
    count = 0
    #model_fields = [f.name for f in data._meta.get_fields()]
    #rows = [ r[0] for r in data if model_fields in field_names ]

    pdf = reportes_pdf('L', 'mm', 'A4',current_user)
    report_fullpath = os.path.join(settings.DATA_PDF_PATH,"vl_reporte_cobranza_saldos.{}.pdf".format(pdf.timestamp))
    pdf.set_title( "Viejos Lobos - reporte Familias" )
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
        logger.debug(row.crm_id)
        count+=1
        cell_v=5
        pdf.cell(col_widths[0], cell_v, str(count), "LR", 0, "L", fill)
        logger.debug("{}-{}".format(row.crm_id,row.familia_crm_id) )
        pdf.cell(col_widths[1], cell_v, str(row.crm_id) , "LR", 0, "L", fill)
        pdf.cell(col_widths[2], cell_v, str(row.familia_crm_id), "LR", 0, "L", fill)
        pdf.cell(col_widths[3], cell_v, str(row.actualizado), "LR", 0, "L", fill)
        pdf.ln()
        fill = not fill
    pdf.cell(page_width, 0, "", "T")
    pdf.output(  report_fullpath)
    return FileResponse(open(report_fullpath, 'rb'), as_attachment=True, content_type='application/pdf')

# reporte_familia_pdf
def reporte_familia_pdf(data):
    ''' Detalle familia'''

    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logger.debug(" %s: %s in %s:%i" % (
        'init ', 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

    logger.debug("PDF DATA SOURCE: {} ".format(data) )
    usuario = data["usuario"]
    familia = data["familia"]
    socios =  data["socios"]
    cuotas =  data["cuotas"]
    cuotas_vencidas =  data["cuotas_vencidas"]
    cuotas_vencidas_suma =  data["cuotas_vencidas_suma"]
    pagos =  data["pagos"]
    pagos_suma =  data["pagos_suma"]
    observaciones = data["observaciones"]

    report_data = (
            ("CRM_ID" , 'familia_crm_id'),
            ("Calle" , 'direccion_calle'),
            ("Numero" , "direccion_numero"),
        )

    cell_v=5
    col_width=200
    fill=False
    
    pdf = reportes_pdf('P', 'mm', 'A4')
    title = "Ficha Familia #{} {}  Fecha {}".format(familia.crm_id, familia.familia_crm_id ,pdf.timestamp) 
    pdf.set_title(title)
    pdf.alias_nb_pages()
    pdf.set_image_filter("DCTDecode")
    pdf.add_page()
    pdf.set_font("Times", size=12)
    
    pdf.cell(col_width, cell_v,  "Usuario: {}   Fecha {}".format(usuario.username ,pdf.timestamp) ,1, 0, "C")
    pdf.ln()
    pdf.cell(col_width, cell_v, "Familia ID: "+str(familia.crm_id) , "LR", 0, "L", fill)
    pdf.ln()
    pdf.cell(col_width, cell_v, "Familia: "+str(familia.familia_crm_id) , "LR", 0, "L", fill)
    pdf.ln()
    depto = "depto "+familia.direccion_depto if familia.direccion_depto else ""
    pdf.cell(col_width, cell_v, "Domicilio: {} {} {}  {},{}".format(
        str(familia.direccion_calle),str(familia.direccion_numero),depto,
        str(familia.direccion_localidad),str(familia.direccion_provincia)
        ) , "LR", 0, "L", fill)
    pdf.ln()
    pdf.cell(col_width, cell_v, "Contacto: "+str(familia.contacto) , "LR", 0, "L", fill)
    pdf.ln()

    pdf.cell(col_width, cell_v, "Socios: " , "LR", 0, "L", fill)
    categorias = { k: v for k,v in Socio.CATEGORIAS_CHOISES} # convertir en metodo de Socio model
    for socio in socios:
        pdf.cell(col_width, cell_v, "      {}, {} - DNI {} - F.Nac {} - CAT {}".format(
            str(socio.apellidos),str(socio.nombres),str(socio.dni),str(socio.fecha_nacimiento),
            str(categorias[socio.categoria] ) 
            ) , "LR", 0, "L", fill)
        pdf.ln()
    pdf.ln()

    #pdf.basic_table(headers,field_names, data)
    #pdf.colored_table(headers,field_names, data)
    #for h in report_data:
    #        pdf.cell(0, 10, h[0] , 0, 1)
    #for i in data:
    #    for h in report_data:
    #        pdf.cell(0, 10, getattr(i,h[1]) , 0, 1)
    pdf.use_footer="pepinos"
    pdf.output(title.replace(" ","_")+"pdf")
    return FileResponse(open(title.replace(" ","_")+"pdf", 'rb'), as_attachment=True, content_type='application/pdf')

def test_report(request):
    sales = [
        {"item": "Keyboard", "amount": "$120,00"},
        {"item": "Mouse", "amount": "$10,00"},
        {"item": "House", "amount": "$1 000 000,00"},
    ]

    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'This is what you have sold this month so far:',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Item'.ljust(30)} {'Amount'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    pdf.output('report.pdf', 'F')
    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')


def reporte_cobranza_pdf(current_user,data,filter_info):
    '''Reporte de pago de cuotas percibidos'''

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



def index(request):

    return None


def socios_familia(familias):

    # continuas TODO 
    return None
