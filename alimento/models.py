from django.db import models
from vacas.models import Vaca
from django.contrib.auth.models import User

# Create your models here.
class Alimento(models.Model):
    # vaca_id = models.IntegerField()
    nombre = models.CharField(max_length=45)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo = models.FloatField(blank=True ,null=True)
    fecha_suministro = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    vaca = models.ForeignKey(Vaca, on_delete = models.CASCADE, null = True)
    usuario = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

class AlimentoExport(models.Model):
    nombre = models.CharField(max_length=45, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_export = models.DateField()
    destino = models.CharField(max_length=200, null=True, blank=True)
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE, blank=True, null=True)