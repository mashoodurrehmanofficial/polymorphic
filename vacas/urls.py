from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name = "vacas"),
    path("add", views.add, name = "vacas.add"),
    path("update/<int:id>", views.update, name = "vacas.update"),
    path("delete/<int:id>", views.delete, name = "vacas.delete"),
    url(r'^ajax-all-vacas/$', views.ajaxallvacas, name='ajax_all_vacas'),
    url(r'^ajax-filter-vacas/$', views.ajaxfiltervacas, name='ajax_filter_vacas'),
    url(r'^ajax-process-vacas/$', views.ajaxprocessvacas, name='ajax_process_vacas'),
    
    url(r'^ajax_raza_add/$', views.ajax_raza_add, name='ajax_raza_add'),

]