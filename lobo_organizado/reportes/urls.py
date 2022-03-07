

from django.urls import path

from . import views

app_name = 'reportes'
urlpatterns = [
    path('test', views.test_report, name='test_reports'),
    path('', views.index, name='index'),
]