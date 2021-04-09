

from django.urls import path

from . import views

app_name = 'socios'
urlpatterns = [
    path('', views.index, name='index'),
    path('socio/<int:socio_id>', views.socio_detalle, name='socio_detalle'),
    path('socio/nuevo/<int:familia_id>', views.socio_nuevo, name='socio_nuevo'),
    path('socio/editar/<int:socio_id>', views.socio_editar, name='socio_editar'),
    path('socio/borrar/<int:socio_id>', views.socio_borrar, name='socio_borrar'),
    path('socios', views.socio_index, name='socios_listado'),
    path('familia/<int:familia_id>', views.familia_detalle, name='familia_detalle'),
    path('familia/<int:familia_id>/<str:error_message>', views.familia_detalle, name='familia_detalle_error'),
    path('familia/nuevo/<int:familia_id>/<str:error_message>', views.familia_nuevo, name='familia_nuevo'),
    path('familia/nuevo/<int:familia_id>', views.familia_nuevo, name='familia_nuevo'),
    path('familia/observacion/editar/<int:observacion_id>', views.familia_observacion_editar, name='familia_editar_observacion'),
    path('familia/observacion/borrar/<int:observacion_id>', views.familia_observacion_borrar, name='familia_borrar_observacion'),
    path('familias/<str:error_message>', views.familia_index, name='familia_listado'),
    path('familias', views.familia_index, name='familia_listado'),
    path('observacion/nuevo/<int:familia_id>/<int:observacion_id>', views.observacion_nuevo, name='observacion_nuevo'),
    path('observacion/borrar/<int:observacion_id>', views.observacion_borrar, name='observacion_borrar'),
]