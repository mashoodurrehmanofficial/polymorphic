from django.db import models
from preñez.models import MetodoPreñez
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Pajuela(MetodoPreñez):
    nombre = models.CharField(max_length=45)
    raza = models.CharField(max_length=45)
    costo = models.FloatField()
    fecha_compra = models.DateField()    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    usuario = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    
    @property
    def dias_compra(self):
        return (datetime.now().date() - self.fecha_compra).days
    
    @property
    def estado(self):
        if self.dias_compra < 90:
            return "Óptimo (" + str(self.dias_compra) + "d)"
        return "Malo (" + str(self.dias_compra) + "d)"