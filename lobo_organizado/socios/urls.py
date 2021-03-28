

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('familia/<int:familia_id>', views.detalle, name='detalle'),
    path('familias', views.familia_index, name='listado'),
]