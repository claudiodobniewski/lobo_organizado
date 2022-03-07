"""lobo_organizado URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    path('accounts/', include('django.contrib.auth.urls')), # new
    path('accounts/login/', auth_views.LoginView.as_view(template_name='lobo_organizado/login.html')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('cuotas/', include('cuotas.urls')),
    path('socios/', include('socios.urls')),
    path('reportes/', include('reportes.urls')),
    path('admin/', admin.site.urls),
    
]
