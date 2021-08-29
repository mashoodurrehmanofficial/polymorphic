from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ValidateCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.code