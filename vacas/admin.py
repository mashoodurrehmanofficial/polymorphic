from django.contrib import admin

# Register your models here.

from vacas.models import Raza, Vaca

admin.site.register(Raza)
admin.site.register(Vaca)
