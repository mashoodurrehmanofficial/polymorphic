from django.db import models
from vacas.models import Vaca
from django.contrib.auth.models import User

# Create your models here.
class Produccion(models.Model):
    # vaca_id = models.IntegerField()
    cantidad = models.FloatField()
    fecha_produccion = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    vaca = models.ForeignKey(Vaca, on_delete = models.CASCADE)
    # calificacion = models.OneToOneField(Calificacion, on_delete = models.CASCADE)
    usuario = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    estimación_de_calidad = models.CharField(max_length=250, blank=True, null=True)
    
class Calificacion(models.Model):
    # produccion_id = models.IntegerField()
    valor = models.FloatField()
    resultado = models.CharField(max_length=50)
    fecha_calificacion = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    produccion = models.OneToOneField(Produccion, on_delete = models.CASCADE)