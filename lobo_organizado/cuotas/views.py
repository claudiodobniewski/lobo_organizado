from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from socios.models import Familia
from cuotas.models import PlanDePago,CuotaPago

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the cuotas index.")

def nuevo_pago(request, familia_id):

    familia_socios = Familia.objects.get(pk=familia_id)

    planes_de_pago = PlanDePago.objects.all()

    #return HttpResponse("Hello, world. ACA VA PANTALLA PAGO NUEVA CUOTA.")
    return render(request, 'cuotas/cuota_nueva.html', {'familia': familia_socios,'planes_de_pago':planes_de_pago})

def procesa_nuevo_pago(request, familia_id):

  
    for param in request.POST:
        print("Param {}={}".format(param,request.POST[param]))

    selected_family = Familia.objects.get(pk=request.POST['familia_id'])
    selected_plan_de_pago = PlanDePago.objects.get(pk=request.POST['plan_de_pago_id'])
    print( "URL param:{} => form param:{} plan_id:{}  plan:{} importe={} ".format(familia_id,selected_family.pk,request.POST['plan_de_pago_id'],selected_plan_de_pago,request.POST['importe_cobrado']))
    if selected_family.pk != familia_id:
        print("no coinciden los id de familia!")
    familia_socios = Familia.objects.get(pk=familia_id)

    planes_de_pago = PlanDePago.objects.get(pk=request.POST['plan_de_pago_id'])

    nuevo_pago = CuotaPago()
    nuevo_pago.importe = request.POST['importe_cobrado']
    nuevo_pago.familia = selected_family
    nuevo_pago.fecha_cobro = request.POST['fecha_cobrado']
    nuevo_pago.aplica_pago_plan = selected_plan_de_pago
    nuevo_pago.save()

    return HttpResponseRedirect(reverse('socios:familia_detalle', args=(selected_family.id,)))


