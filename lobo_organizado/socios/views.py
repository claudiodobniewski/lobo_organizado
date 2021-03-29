from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Familia, Socio


def index(request):
    return HttpResponse("Hello, world. You're at the socios index.")

def familia_index(request):

    lista_familias = Familia.objects.all()
    output = ', '.join([fam.familia_crm_id for fam in lista_familias])
    print(lista_familias)
    return render(request, 'socios/familia_listado.html', {'familias': lista_familias})

def detalle(request, familia_id):
    
    try:
        familia_socios = Familia.objects.get(pk=familia_id)
        socios = Socio.objects.filter(familia_id=familia_socios.id)
        print(socios)
    except Exception as err:
        raise Http404("Unexpected error: {0}".format(err))
    return render(request, 'socios/familia_detalle.html', {'familia': familia_socios,'socios':socios})
