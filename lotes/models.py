from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lote(models.Model):
    
    nombre = models.CharField(max_length=45)
    carga = models.IntegerField()
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    usuario = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    
    @property
    def tiempo_uso(self):
        start = self.fecha_entrada
        end = self.fecha_salida        
        return str((end - start).days) + " días"