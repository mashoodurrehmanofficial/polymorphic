from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name = "crias"),
    path("add", views.add, name = "crias.add"),
    path("update/<int:id>", views.update, name = "crias.update"),
    path("delete/<int:id>", views.delete, name = "crias.delete"),
    url(r'^ajax_date_check/$', views.ajax_date_check, name='ajax_date_check'),

]