

from django.urls import path

from . import views

app_name = 'cuotas'
urlpatterns = [
    path('familia/nuevo_pago/<int:familia_id>', views.nuevo_pago, name='nuevo_pago'),
    path('', views.index, name='index'),
]