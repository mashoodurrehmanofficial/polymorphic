from django.db import models
from vacas.models import Vaca
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Cria(models.Model):
    # vaca_id = models.IntegerField()
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=45)
    nacimiento = models.CharField(max_length=45)
    destino = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    vaca_madura_id = models.IntegerField(null = True)
    nombre = models.CharField(max_length=100, null = True)
    raza = models.CharField(max_length=45, null = True, blank=True)

    vaca = models.ForeignKey(Vaca, on_delete = models.CASCADE)
    usuario = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    
    @property
    def edad(self):
        born = self.fecha_nacimiento
        today = date.today()
        # print >>sys.stderr, today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return str(today.year - born.year - ((today.month, today.day) < (born.month, born.day))) + " años"    
    