from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "pajuelas"),
    path("add", views.add, name = "pajuelas.add"),
    path("update/<int:id>", views.update, name = "pajuelas.update"),
    path("delete/<int:id>", views.delete, name = "pajuelas.delete"),
]