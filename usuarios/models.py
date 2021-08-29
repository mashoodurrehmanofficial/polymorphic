from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UsuarioInfo(models.Model):
    foto = models.TextField(null = True)
    usuario = models.OneToOneField(User, on_delete = models.CASCADE)
    
    @property
    def foto_url(self):
        return "/static/uploads/usuarios/" + str(self.id) + "/" + self.foto    
    