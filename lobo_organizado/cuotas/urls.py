

from django.urls import path

from . import views

app_name = 'cuotas'
urlpatterns = [
    path('familia/nuevo_pago/<int:familia_id>/<int:pago_id>', views.nuevo_pago, name='nuevo_pago'),
    path('familia/procesa_nuevo_pago/<int:familia_id>', views.procesa_nuevo_pago, name='procesa_nuevo_pago'),
    path('familia/editar_pago/<int:pago_id>', views.editar_pago, name='editar_pago'),
    path('familia/borrar_pago/<int:pago_id>', views.borrar_pago, name='borrar_pago'),
    path('familia/nueva_cuota/<int:familia_id>', views.nueva_cuota, name='nueva_cuota'),
    path('familia/nuevo_cuotas_plan/<int:familia_id>/<int:plan_pagos_id>', views.nuevo_cuotas_plan, name='nuevo_cuotas_plan'),
    path('familia/nuevo_cuotas_plan_seleccion/<int:familia_id>', views.nuevo_cuotas_plan_seleccion, name='nuevo_cuotas_plan_seleccion'),
    path('familia/procesa_nueva_cuota/<int:familia_id>', views.procesa_nueva_cuota, name='procesa_nueva_cuota'),
    path('familia/editar_cuota/<int:cuota_id>', views.editar_cuota, name='editar_cuota'),
    path('familia/borrar_cuota/<int:cuota_id>', views.borrar_cuota, name='borrar_cuota'),
    path('', views.index, name='index'),
]