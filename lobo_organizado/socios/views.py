from django.shortcuts import render

from django.http import HttpResponse
from .models import Familia

def index(request):
    return HttpResponse("Hello, world. You're at the socios index.")

def familia_index(request):

    lista_familias = Familia.objects.all()
    output = ', '.join([fam.familia_crm_id for fam in lista_familias])
    return HttpResponse(output)

def detalle(request, familia_id):
    
    try:
        familia = Familia.objects.get(pk=familia_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'familia_detalle.html', {'familia': familia})
