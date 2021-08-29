from django.db import models
from preñez.models import MetodoPreñez
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Toro(MetodoPreñez):

    Muerte = 'Muerte'
    Venta = 'Venta'
    Process = (
        ('Venta', 'Venta'),
        ('Muerte', 'Muerte'),
    )
    nombre = models.CharField(max_length=45)
    raza = models.CharField(max_length=45)
    fecha_nacimiento = models.DateField()
    # edad = models.IntegerField()
    fecha_compra = models.DateField()
    fecha_primer_monta = models.DateField()
    estado = models.CharField(max_length=45)
    motivo_estado = models.CharField(max_length=255)
    foto = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    costo = models.FloatField(null = True)
    
    usuario = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
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
        return "/static/uploads/toros/" + str(self.id) + "/" + self.foto