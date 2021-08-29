from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("", views.home, name = "reportes"),
    path("crias_toro", views.criasToro, name = "crias_toro"),
    path("crias_produccion_vaca", views.criasProduccionVaca, name = "crias_produccion_vaca"),
    path("crias_vaca", views.criasVaca, name = "crias_vaca"),
    path("crias_data", views.criasData, name = "crias_data"),
    path("preñez_vaca", views.preñezVaca, name = "preñez_vaca"),
    path("pajuelas_buen_estado", views.pajuelasBuenEstado, name = "pajuelas_buen_estado"),
    path("pajuelas_mal_estado", views.pajuelasMalEstado, name = "pajuelas_mal_estado"),
    path("pajuelas_costo", views.pajuelascosto, name = "pajuelas_costo"),
    path("costo_toro", views.costoToros, name = "costo_toro"),
    path("ajax_toro", views.torosajax, name = "ajax_toro"),
    path("toros_activos", views.torosActivos, name = "toros_activos"),
    path("toros_descartados", views.torosDescartados, name = "toros_descartados"),
    path("lote_vacas", views.loteVacas, name = "lote_vacas"),
    path("ajax_lote_vacas", views.ajaxloteVacas, name = "ajax_lote_vacas"),
    path("vacas_y_crías", views.vacasycrías, name = "vacas_y_crías"),
    path("possible_pregnant", views.possiblepregnant, name = "possible_pregnant"),
    path("dados_de_baja", views.dadosdebaja, name = "dados_de_baja"),
    url(r'^ajax-filter-produccion-vaca/$', views.ajaxfilterproduccionvacas, name='ajax_filter_produccion_vaca'),
    url(r'^graphic_production/$', views.graphic_production, name='graphic_production'),
    url(r'^ajax_filter_graphic/$', views.ajax_filter_graphic, name='ajax_filter_graphic')
]