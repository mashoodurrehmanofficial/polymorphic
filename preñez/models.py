from django.db import models
from vacas.models import Vaca
from polymorphic.models import PolymorphicModel
from django.contrib.auth.models import User
   
class MetodoPreñez(PolymorphicModel):
    pass

# Create your models here.
class Preñez(models.Model):
    fecha_preñez = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    vaca = models.ForeignKey(Vaca, on_delete = models.CASCADE)
    fecundaciones = models.ManyToManyField(MetodoPreñez, related_name = "fecundaciones")
    usuario = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)



    