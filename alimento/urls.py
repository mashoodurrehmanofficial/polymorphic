from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name = "alimento"),
    path("add", views.add, name = "alimento.add"),
    path("update/<int:id>", views.update, name = "alimento.update"),
    path("export", views.export, name = "alimento.export"),
    path("delete/<int:id>", views.delete, name = "alimento.delete"),
    url(r'^ajax-all-alimento/$', views.ajaxallalimento, name='ajax_all_alimento'),
    url(r'^ajax-filter-alimento/$', views.ajaxfilteralimento, name='ajax_filter_alimento'),
    url(r'^ajaxgetalimento/$', views.ajaxgetalimento, name='ajax_get_alimento'),
    url(r'^ajaxalimentoexport/$', views.ajaxalimentoexport, name='ajaxalimentoexport'),
]