from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name = "toros"),
    path("add", views.add, name = "toros.add"),
    path("update/<int:id>", views.update, name = "toros.update"),
    path("delete/<int:id>", views.delete, name = "toros.delete"),
    url(r'^ajax-process-toro/$', views.ajaxprocesstoro, name='ajax_process_toro'),
]