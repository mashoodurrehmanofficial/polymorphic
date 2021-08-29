from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "preñez"),
    path("add", views.add, name = "preñez.add"),
    path("update/<int:id>", views.update, name = "preñez.update"),
    path("delete/<int:id>", views.delete, name = "preñez.delete"),
    path("getToros", views.getToros, name = "obtenerToros"),
    path("getPajuelas", views.getPajuelas, name = "obtenerPajuelas"),
]