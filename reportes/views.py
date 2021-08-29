from produccion.models import Produccion
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from datetime import date
import shutil
from django.contrib.auth.decorators import login_required

from django.utils.timesince import timesince
from django.db.models import Sum, Count
from toros.models import Toro
from vacas.models import Vaca
from preñez.models import Preñez
from pajuelas.models import Pajuela
from lotes.models import Lote
import dateutil.parser
from crias.models import Cria 
from django.db.models import Q

@login_required(login_url='/auth/login')
def home(request):
    vacas = Vaca.objects.all()
    current_time = date.today()
    lotes = Lote.objects.all()
    toros = Toro.objects.all()
    return render(request, "reportes/home.html",{ "current_time" : current_time, 'vacas': vacas, 'lotes':lotes, 'toros':toros })

@login_required(login_url='/auth/login')
def criasToro(request):
    toros = Toro.objects.all()
    data = []
    headers = [
        {"title" : "Toro"},
        {"title" : "Tiempo de Servicio"},
        {"title" : "No. de Crías"}
    ]
    for toro in toros:
        data.append([
            toro.nombre,
            timesince(toro.fecha_compra),
            toro.fecundaciones.count()
        ])
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    )

@login_required(login_url='/auth/login')
def criasProduccionVaca(request):
    vacas = Vaca.objects.all()
    data = [];
    headers = [
        {"title" : "Vaca"},
        {"title" : "Producción"},
        {"title" : "No. de Crías"}
    ];
    for vaca in vacas:
        cantidad = vaca.produccion_set.aggregate(cantidad = Sum("cantidad"))["cantidad"]
        data.append([
            vaca.nombre,
            str(cantidad) + " Litros" if cantidad is not None else "",
            vaca.cria_set.count()
        ])
    return JsonResponse({ 
            "headers" : headers,
            "data" : data,
        }, 
        safe = False
    )

def ajaxfilterproduccionvacas(request):
    if request.method == "POST":
        razas = request.POST.get("razas")
        edad = request.POST.get("edad")
        daterange = request.POST.get("daterange")

        if razas != "" and edad == "" and daterange == "":
            vacas = Vaca.objects.filter(raza__contains=razas)
        elif razas != "" and edad != "" and daterange == "":
            format_str = '%d%m%Y'
            edad_obj = datetime.strptime(edad, format_str)
            
            vacas = Vaca.objects.filter(fecha_nacimiento=edad_obj, raza__contains=razas)
        elif razas != "" and edad != "" and daterange != "":
            format_str = '%d%m%Y'
            edad_obj = datetime.strptime(edad, format_str)
            
            vacas = Vaca.objects.filter(fecha_nacimiento=edad_obj, raza__contains=razas)
        elif razas == "" and edad != "" and daterange == "":
            format_str = '%d%m%Y'
            edad_obj = datetime.strptime(edad, format_str)
            vacas = Vaca.objects.filter(fecha_nacimiento=edad_obj)
        elif razas == "" and edad != "" and daterange != "":
            format_str = '%d%m%Y'
            edad_obj = datetime.strptime(edad, format_str)
            vacas = Vaca.objects.filter(fecha_nacimiento=edad_obj)
        elif razas != "" and edad == "" and daterange != "":
            vacas = Vaca.objects.filter(raza__contains=razas)
        else:
            vacas = Vaca.objects.all()
        data = []
        headers = [
            {"title" : "Vaca"},
            {"title" : "Producción"},
            {"title" : "No. de Crías"}
        ]

        for vaca in vacas:
            if daterange != "":
                format_str = '%d%m%Y'
                start_date = daterange.split("-")[0].strip().replace(".", "")
                end_date = daterange.split("-")[1].strip().replace(".", "")
                start_obj = datetime.strptime(start_date, format_str)
                end_obj = datetime.strptime(end_date, format_str)
                cantidad = Produccion.objects.filter(vaca_id=vaca.id, fecha_produccion__gte=start_obj, fecha_produccion__lte=end_obj).aggregate(Sum("cantidad"))["cantidad__sum"]
            else:
                cantidad = vaca.produccion_set.aggregate(cantidad = Sum("cantidad"))["cantidad"]
            data.append([
                vaca.nombre,
                str(cantidad) + " Litros" if cantidad is not None else 0,
                vaca.cria_set.count()
            ])
        return JsonResponse({ 
                "headers" : headers,
                "data" : data,
            }, 
            safe = False
        )

@login_required(login_url='/auth/login')
def criasVaca(request):
    vacas = Vaca.objects.all()
    data = [];
    headers = [
        {"title" : "Vaca"},
        {"title" : "Cría"},
    ];
    for vaca in vacas:        
        data.append([
            vaca.nombre,
            str(vaca.cria_set.count()) + (" crías" if vaca.cria_set.count() != 1 else " cría")
        ])
        for cria in vaca.cria_set.all():
            data.append([
                '',
                cria.nombre,                
            ])  
        
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    )

@login_required(login_url='/auth/login')
def criasData(request):
    crias = Cria.objects.all()
    data = [];
    headers = [
        {"title" : "Nombre"},
        {"title" : "Nacimiento"},
        {"title" : "Destino"},
        {"title" : "Fecha Nacimiento"},
    ];
    for cria in crias:        
        data.append([
            cria.nombre,
            cria.nacimiento,
            cria.destino,
            cria.fecha_nacimiento.strftime('%d %b, %Y'),

        ])
        
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    )
    
@login_required(login_url='/auth/login')
def preñezVaca(request):
    
    vacas_id = [x.id for x in Vaca.objects.all() if x.tiempo_preñez is not None]
    vacas = Vaca.objects.filter(id__in = vacas_id)
    
    data = [];
    headers = [
        {"title" : "Vaca"},
        {"title" : "Tiempo en preñez"},
    ];
    for vaca in vacas:        
        data.append([
            vaca.nombre,
            vaca.tiempo_preñez
        ])        
        
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    )

@login_required(login_url='/auth/login')
def possiblepregnant(request):
    today = date.today()
    a_month = dateutil.relativedelta.relativedelta(months = 16)
    fecha_date = today - a_month
    a_date = dateutil.relativedelta.relativedelta(days = 45)
    fecha_crias = today - a_date
    vacas = Vaca.objects.filter(fecha_nacimiento__gte=fecha_date).exclude(~Q(processm=None))
    crias = Cria.objects.filter(fecha_nacimiento__gte=fecha_crias)

    data = []
    headers = [
        {"title" : "Nombre"},
        {"title" : "Raza"},
    ]

    for vaca in vacas:
        data.append([
            vaca.nombre,
            vaca.raza
        ]) 
    for cria in crias:
       data.append([
            cria.nombre,
            cria.raza
        ]) 

    return JsonResponse({ 
            "headers" : headers,
            "data" : data,
        }, 
        safe = False
    )

@login_required(login_url='/auth/login')
def dadosdebaja(request):
    vacas = Vaca.objects.filter(~Q(processm=None))
    toros = Toro.objects.filter(~Q(processm=None))
    data = []
    headers = [
        {"title" : "Nombre"},
        {"title" : "Raza"},
        {"title": "Fecha"},
        {"title": "Objetivo"},
        {'title': "Razón"}
    ]

    for vaca in vacas:
        data.append([
            vaca.nombre,
            vaca.raza,
            vaca.fecha_processm,
            vaca.processm, 
            vaca.reason
        ]) 

    for toro in toros:
        data.append([
            toro.nombre,
            toro.raza,
            toro.fecha_processm,
            toro.processm,
            toro.reason
        ]) 

    return JsonResponse({ 
            "headers" : headers,
            "data" : data,
        }, 
        safe = False
    )
    


    
@login_required(login_url='/auth/login')
def vacasycrías(request):
    prenez = Preñez.objects.all()
    prenez_to_exclude = [o.vaca_id for o in prenez] 
    arr_vacas = []
    today = date.today()
    a_month = dateutil.relativedelta.relativedelta(months = 16)
    a_date = dateutil.relativedelta.relativedelta(days = 45)
    fecha_menos = today - a_month
    fecha_date = today - a_date
    vacas = Vaca.objects.filter(fecha_nacimiento__gte=fecha_menos, fecha_nacimiento__lte=fecha_date).exclude(id__in=prenez_to_exclude)
    crias = Cria.objects.filter(fecha_nacimiento__gte=fecha_menos, fecha_nacimiento__lte=fecha_date, sexo="Hembra", nacimiento="Vivo")
    arr_vacas.extend(vacas)
    arr_vacas.extend(crias)
    
    headers = [
        {"title" : "Nombre"},
        {"title" : "para proceso de preñar"},
    ]
    data = []
    for vaca in arr_vacas:
        
        tiempo_preñez = "Estos animales necesitan entrar en preñez"
        data.append([
            vaca.nombre,
            tiempo_preñez
        ]) 
    if len(data) != 0:           
        return JsonResponse({ 
                "headers" : headers,
                "data" : data,
                "message": "Estos animales necesitan entrar en preñez!"
            }, 
            safe = False
        )
    else:
        return JsonResponse({ 
                "headers" : headers,
                "data" : data,
            }, 
            safe = False
        )


@login_required(login_url='/auth/login')
def pajuelasBuenEstado(request):
        
    pajuelas_id = [x.id for x in Pajuela.objects.all() if x.dias_compra < 90]
    pajuelas = sorted(Pajuela.objects.filter(id__in = pajuelas_id), key = lambda t: t.dias_compra)
    
    data = [];
    headers = [
        {"title" : "Pajuela"},        
        {"title" : "Estado"},
    ];
    for pajuela in pajuelas:        
        data.append([
            pajuela.nombre,            
            pajuela.estado
        ])        
        
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    )
    
@login_required(login_url='/auth/login')
def pajuelasMalEstado(request):
        
    pajuelas_id = [x.id for x in Pajuela.objects.all() if x.dias_compra >= 90]
    pajuelas = sorted(Pajuela.objects.filter(id__in = pajuelas_id), key = lambda t: t.dias_compra)
    
    data = [];
    headers = [
        {"title" : "Pajuela"},        
        {"title" : "Estado"},
    ];
    for pajuela in pajuelas:        
        data.append([
            pajuela.nombre,            
            pajuela.estado
        ])        
        
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    )
    
@login_required(login_url='/auth/login')
def torosActivos(request):
            
    toros = Toro.objects.filter(estado = "Activo")
    
    data = [];
    headers = [
        {"title" : "Toro"},        
        {"title" : "Estado"},
    ];
    for toro in toros:        
        data.append([
            toro.nombre,            
            toro.estado
        ])        
        
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    )
    
@login_required(login_url='/auth/login')
def torosDescartados(request):
        
    toros = Toro.objects.filter(estado = "Descartado")
    
    data = [];
    headers = [
        {"title" : "Toro"},        
        {"title" : "Estado"},
    ];
    for toro in toros:        
        data.append([
            toro.nombre,            
            toro.estado
        ])        
        
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    )
    
@login_required(login_url='/auth/login')
def loteVacas(request):
        
    lotes = Lote.objects.all()
    
    data = []
    headers = [
        {"title" : "Lote"},        
        {"title" : "Carga"},
        {"title" : "Ingreso"},
        {"title" : "Salida"},
        {"title" : "Tiempo de uso"},
        {"title" : "Estado"},
    ]
    for lote in lotes: 
        if int(lote.tiempo_uso.replace("días", "").strip()) >= 29:
            status = "descanso ideal"
        else:
            status = " Falta  " +  str(30 - int(lote.tiempo_uso.replace("días", "").strip())) +  "días"

        data.append([
            lote.nombre,            
            lote.carga,
            lote.fecha_entrada,
            lote.fecha_salida,
            lote.tiempo_uso,
            status
        ])        
        
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    )

@login_required(login_url='/auth/login')
def costoToros(request):
    toros = Toro.objects.all()
    
    data = []
    headers = [
        {"title" : "Nombre"},        
        {"title" : "Raza"},
        {"title" : "Edad"},
        {"title" : "Costo"},
    ]

    for toro in toros:
        born = toro.fecha_nacimiento
        today = date.today()
        edad = ''
        edad_val = dateutil.relativedelta.relativedelta(today, born)
        if edad_val.years and edad_val.months and edad_val.days:
            edad += str(edad_val.years) + " años " + str(edad_val.months) + " meses " + str(edad_val.days//7) + " semanas"
        elif edad_val.months and edad_val.days:
            if edad_val.days > 7:
                edad += str(edad_val.months) + " meses " + str(edad_val.days//7) + " semanas"
            else:
                edad += str(edad_val.months) + " meses "
        elif edad_val.days:
            if edad_val.days > 7:
                edad += str(edad_val.days//7) + " semanas"
        else:
            edad = ''

        data.append([
            toro.nombre,            
            toro.raza,
            edad,
            toro.costo,
        ])

    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    ) 

    
def ajaxloteVacas(request):
    if request.method == "POST":
        lotes_v = request.POST.getlist('lotes[]')
        lote_arr = []
        data = []
        headers = [
            {"title" : "Lote"},        
            {"title" : "Carga"},
            {"title" : "Ingreso"},
            {"title" : "Salida"},
            {"title" : "Tiempo de uso"},
            {"title" : "Estado"},
        ]
        for lo_v in lotes_v:
            lote_arr.append(Lote.objects.filter(nombre__contains=lo_v))

        for lote_aa in lote_arr:
            for lote_a in lote_aa:
                if int(lote_a.tiempo_uso.replace("días", "").strip()) >= 29:
                    status = "ideal para rotacion"
                else:
                    status = str(29 - int(lote_a.tiempo_uso.replace("días", "").strip())) + "  días"

                data.append([
                    lote_a.nombre,            
                    lote_a.carga,
                    lote_a.fecha_entrada,
                    lote_a.fecha_salida,
                    lote_a.tiempo_uso,
                    status
                ])  

        return JsonResponse({ 
                "headers" : headers,
                "data" : data
            }, 
            safe = False
        )

def torosajax(request):
    if request.method == "POST":
        raza = request.POST.get('raza')
        edad = request.POST.get('edad')
        data = []
        if len(raza) != 0 and edad == "":
            toros_s = Toro.objects.filter(raza=raza).values('raza').annotate(Sum('costo'), Count('raza'))
            headers = [       
                {"title" : "Raza"},
                {"title" : "Costo"},
                {"title" : "Contar"},
            ]
            for toro_s in toros_s:

                data.append([          
                    toro_s['raza'],
                    toro_s['costo__sum'],
                    toro_s['raza__count'],
                ])
        elif raza != "" and edad != "":
            format_str = '%d%m%Y'
            date_obj = datetime.strptime(edad, format_str)
            toros_s = Toro.objects.filter(raza=raza,fecha_nacimiento__gte=date_obj).values('raza', 'fecha_nacimiento').annotate(Sum('costo'), Count('raza'))
            headers = [     
                {"title" : "Raza"},  
                {"title" : "Edad"},
                {"title" : "Costo"},
                {"title" : "Contar"},
            ]

            for toro_s in toros_s:
                born = toro_s['fecha_nacimiento']
                today = date.today()
                edad = ''
                edad_val = dateutil.relativedelta.relativedelta(today, born)
                if edad_val.years and edad_val.months and edad_val.days:
                    edad += str(edad_val.years) + " años " + str(edad_val.months) + " meses " + str(edad_val.days//7) + " semanas"
                elif edad_val.months and edad_val.days:
                    if edad_val.days > 7:
                        edad += str(edad_val.months) + " meses " + str(edad_val.days//7) + " semanas"
                    else:
                        edad += str(edad_val.months) + " meses "
                elif edad_val.days:
                    if edad_val.days > 7:
                        edad += str(edad_val.days//7) + " semanas"
                else:
                    edad = ''

                data.append([ 
                    toro_s['raza'] ,      
                    edad,
                    toro_s['costo__sum'],
                    toro_s['raza__count'],
                ])
        elif len(raza) == 0 and edad != "":
            format_str = '%d%m%Y'
            date_obj = datetime.strptime(edad, format_str)
            toros_s = Toro.objects.filter(fecha_nacimiento__gte=date_obj).values('fecha_nacimiento').annotate(Sum('costo'), Count('raza'))
            headers = [       
                {"title" : "Edad"},
                {"title" : "Costo"},
                {"title" : "Contar"},
            ]
            for toro_s in toros_s:
                born = toro_s['fecha_nacimiento']
                today = date.today()
                edad = ''
                edad_val = dateutil.relativedelta.relativedelta(today, born)
                if edad_val.years and edad_val.months and edad_val.days:
                    edad += str(edad_val.years) + " años " + str(edad_val.months) + " meses " + str(edad_val.days//7) + " semanas"
                elif edad_val.months and edad_val.days:
                    if edad_val.days > 7:
                        edad += str(edad_val.months) + " meses " + str(edad_val.days//7) + " semanas"
                    else:
                        edad += str(edad_val.months) + " meses "
                elif edad_val.days:
                    if edad_val.days > 7:
                        edad += str(edad_val.days//7) + " semanas"
                else:
                    edad = ''

                data.append([          
                    edad,
                    toro_s['costo__sum'],
                    toro_s['raza__count'],
                ])
        else:
            
            toros_s = Toro.objects.all().values('raza', 'fecha_nacimiento').annotate(Sum('costo'), Count('raza'))
            headers = [     
                {"title" : "Raza"},  
                {"title" : "Edad"},
                {"title" : "Costo"},
                {"title" : "Contar"},
            ]

            for toro_s in toros_s:
                born = toro_s['fecha_nacimiento']
                today = date.today()
                edad = ''
                edad_val = dateutil.relativedelta.relativedelta(today, born)
                if edad_val.years and edad_val.months and edad_val.days:
                    edad += str(edad_val.years) + " años " + str(edad_val.months) + " meses " + str(edad_val.days//7) + " semanas"
                elif edad_val.months and edad_val.days:
                    if edad_val.days > 7:
                        edad += str(edad_val.months) + " meses " + str(edad_val.days//7) + " semanas"
                    else:
                        edad += str(edad_val.months) + " meses "
                elif edad_val.days:
                    if edad_val.days > 7:
                        edad += str(edad_val.days//7) + " semanas"
                else:
                    edad = ''

                data.append([ 
                    toro_s['raza'] ,      
                    edad,
                    toro_s['costo__sum'],
                    toro_s['raza__count'],
                ])
        

        return JsonResponse({ 
                "headers" : headers,
                "data" : data
            }, 
            safe = False
        ) 

@login_required(login_url='/auth/login')
def pajuelascosto(request):
    data = []

    headers = [  
        {"title" : "Nombre"},    
        {"title" : "Raza"},  
        {"title" : "Costo"},
        {"title" : "Contar"},
    ]

    pajuelas = Pajuela.objects.values('raza', 'nombre').annotate(Sum('costo'), Count('raza'))

    for paj in pajuelas:
        data.append([ 
            paj['nombre'] ,      
            paj['raza'] , 
            paj['costo__sum'],
            paj['raza__count'],
        ])
    return JsonResponse({ 
            "headers" : headers,
            "data" : data
        }, 
        safe = False
    ) 

def ajax_filter_graphic(request):
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        sum_product = Produccion.objects.filter(fecha_produccion=fecha).values('vaca_id').annotate(Sum('cantidad'))
        arr_name = []
        arr_cantidad = []
        arr_use = []
        for s_product in sum_product:
            vaca = Vaca.objects.get(id=s_product['vaca_id'])
            arr_name.append(vaca.nombre)
            
            arr_cantidad.append(int(float(s_product['cantidad__sum'])))
        return render(request, "reportes/ajax-production.html",{ 'g_name': arr_name,'g_cantidad': arr_cantidad, 'fecha': fecha,'g_use': arr_use  })

def graphic_production(request):
    if request.method == "POST":
        sum_product = Produccion.objects.values('vaca_id').annotate(Sum('cantidad'))
        arr_name = []
        arr_cantidad = []
        arr_use = []
        for s_product in sum_product:
            vaca = Vaca.objects.get(id=s_product['vaca_id'])
            arr_name.append(vaca.nombre)
            arr_cantidad.append(int(float(s_product['cantidad__sum'])))
        return render(request, "reportes/ajax-production.html",{ 'g_name': arr_name,'g_cantidad': arr_cantidad  })

    