from django.contrib import admin

from .models import Familia
from .models import Socio

admin.site.register(Familia)
admin.site.register(Socio)