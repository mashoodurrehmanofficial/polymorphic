from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "lotes"),
    path("add", views.add, name = "lotes.add"),
    path("update/<int:id>", views.update, name = "lotes.update"),
    path("delete/<int:id>", views.delete, name = "lotes.delete"),
]