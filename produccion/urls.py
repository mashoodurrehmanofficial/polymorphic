from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name = "produccion"),
    path("add", views.add, name = "produccion.add"),
    path("update/<int:id>", views.update, name = "produccion.update"),
    path("delete/<int:id>", views.delete, name = "produccion.delete"),
    url(r'^ajax-all-produccion/$', views.ajaxallproduccion, name='ajax_all_produccion'),
    url(r'^ajax-filter-produccion/$', views.ajaxfilterproduccion, name='ajax_filter_produccion'),
]