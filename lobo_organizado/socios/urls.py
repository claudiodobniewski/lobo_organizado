

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('socio/<int:socio_id>', views.socio_detalle, name='socio_detalle'),
    path('socios', views.socio_index, name='socio_listado'),
    path('familia/<int:familia_id>', views.familia_detalle, name='familia_detalle'),
    path('familias', views.familia_index, name='familia_listado'),
]