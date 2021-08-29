from django.db import models
# from crias.models import Cria
# from preñez.models import Preñez
from django.contrib.auth.models import User
from datetime import date
from django.utils.timesince import timesince
import dateutil.parser
from datetime import datetime

# Create your models here.
class Vaca(models.Model):

    Muerte = 'Muerte'
    Venta = 'Venta'
    Process = (
        ('Venta', 'Venta'),
        ('Muerte', 'Muerte'),
    )
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    # edad = models.IntegerField()
    # tiempo_preñez = models.IntegerField()
    foto = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)    
    
    # crias = models.models.ForeignKey(Cria, on_delete = models.CASCADE)
    usuario = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    # fecundaciones = models.ForeignKey(Preñez)
    processm = models.CharField(max_length=20, choices=Process, null=True)
    fecha_processm = models.DateField(null=True)
    reason = models.TextField(blank=True, null=True)

    @property
    def edad(self):
        born = self.fecha_nacimiento
        today = date.today()
        # print >>sys.stderr, today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return str(today.year - born.year - ((today.month, today.day) < (born.month, born.day))) + " años"

    @property
    def foto_url(self):
        return "/static/uploads/vacas/" + str(self.id) + "/" + self.foto
    
    @property
    def tiempo_preñez(self):
        
        # buscamos los registros que tengan menos de 9 meses
        today = date.today()
        a_month = dateutil.relativedelta.relativedelta(months = 9)
        fecha_menos = today - a_month
        
        collection = self.preñez_set.filter(fecha_preñez__gt = fecha_menos)
        
        if collection.count() > 0:
            preñez = collection.latest("fecha_preñez")
            return timesince(preñez.fecha_preñez)        
        
        return None
    
    @property
    def preñez_pasada(self):
        
        # buscamos los registros que tengan menos de 9 meses
        today = date.today()
        a_month = dateutil.relativedelta.relativedelta(months = 9)
        fecha_menos = today - a_month
        
        collection = self.preñez_set.all()
        return collection.count()
        if collection.count() > 0:
            preñez = collection.latest("fecha_preñez")
            delta = datetime.now().date() - preñez.fecha_preñez
            return True if delta.days > 270 else False
        
        return False

class Raza(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        return self.nombre


class BornHistory(models.Model):
    vaca = models.ForeignKey(Vaca, on_delete = models.SET_NULL, null = True)
    fecha = models.DateField(null=True, blank=True)
    


        