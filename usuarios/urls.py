from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "usuarios"),
    path("add", views.add, name = "usuarios.add"),
    path("update/<int:id>", views.update, name = "usuarios.update"),
    path("delete/<int:id>", views.delete, name = "usuarios.delete"),
    path("generateCode", views.generateCode, name = "generateCode"),
]