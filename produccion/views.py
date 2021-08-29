from django.shortcuts import render, redirect
from alimento.models import Alimento
from .models import Produccion
from .models import Calificacion
from vacas.models import Vaca, BornHistory
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Sum
import sys
from django.contrib.auth.decorators import login_required
from datetime import date
import dateutil.parser

@login_required(login_url='/auth/login')
def home(request):
    producciones = Produccion.objects.all()    
    return render(request, "produccion/home.html", { "producciones": producciones })

@login_required(login_url='/auth/login')
def update(request, id):
    
    if not request.user.has_perm('produccion.change_produccion'):
        return redirect("/produccion")
    
    if request.method == "POST":
        vaca_id = request.POST["vaca_id"]
        cantidad = request.POST["cantidad"]
        fecha_produccion = request.POST["fecha_produccion"]
        Produccion.objects.filter(id = id).update(
                            vaca_id = vaca_id,
                            cantidad = cantidad,
                            fecha_produccion = fecha_produccion,
                            usuario_id = request.user.id,
                            updated_at = datetime.now())
        calificacion = Calificacion.objects.filter(produccion_id = id).update(
            valor = 1,
            updated_at = datetime.now()
        )
        messages.success(request, "Registro actualizado")
        return redirect("/produccion")
    produccion = Produccion.objects.get(id = id)
    vacas_id = [x.id for x in Vaca.objects.all() if x.tiempo_preñez is not None]
    vacas = Vaca.objects.all().exclude(id__in = vacas_id)
    return render(request, "produccion/update.html", { "vacas": vacas, "produccion": produccion })

@login_required(login_url='/auth/login')
def add(request):
    today = date.today()
    a_month = dateutil.relativedelta.relativedelta(months = 7)
    adate = today - a_month
    vacas_id = [x.id for x in Vaca.objects.all() if x.tiempo_preñez is not None]
    born_id = [x.vaca_id for x in BornHistory.objects.filter(fecha__gte=adate)]
    vacas = Vaca.objects.filter(id__in = born_id).exclude(id__in = vacas_id)
    
    if request.method == "POST":
        
        vaca_id = request.POST["vaca_id"]
        cantidad = request.POST["cantidad"]
        fecha_produccion = request.POST["fecha_produccion"]

        produccion_check_daily = Produccion.objects.filter(fecha_produccion = fecha_produccion, vaca_id=vaca_id)
        if produccion_check_daily.exists():
            messages.error(request, "Ya se han registrados las 1 producciones del día en la vaca elegida")
            return render(request, "produccion/add.html", { "vacas": vacas })
        
        total_producciones = Produccion.objects.filter(fecha_produccion = fecha_produccion).count()
        
        if total_producciones == 2:
            messages.error(request, "Ya se han registrados las 2 producciones del día en la vaca elegida")
            return render(request, "produccion/add.html", { "vacas": vacas })
        
        produccion = Produccion.objects.create(
                                vaca_id = vaca_id,
                                cantidad = cantidad,
                                fecha_produccion = fecha_produccion
                            )
        produccion.usuario = request.user
        if int(cantidad) > 19:
            estimation = "excelente"
        elif int(cantidad) > 14 and int(cantidad) < 20:
            estimation = "aceptable"
        elif int(cantidad) > 9 and int(cantidad) < 15:
            estimation = "por mejorar"
        else:
            estimation = "producción mal"

        produccion.estimación_de_calidad = estimation
        produccion.save()
        
        filter = Produccion.objects.filter(vaca_id = vaca_id, id__lt = produccion.id);
        last_produccion = None
        
        if filter.exists():
            last_produccion = filter.latest("fecha_produccion")
        
        cantidad_alimentos = 0
        
        if last_produccion != None:
            cantidad_alimentos = Alimento.objects.filter(vaca_id = vaca_id, fecha_suministro__gt = last_produccion.fecha_produccion, fecha_suministro__lte = produccion.fecha_produccion).aggregate(Sum("cantidad"))["cantidad__sum"]
        else:
            cantidad_alimentos = Alimento.objects.filter(vaca_id = vaca_id, fecha_suministro__lte = produccion.fecha_produccion).aggregate(Sum("cantidad"))["cantidad__sum"]
            
        # print >>sys.stderr, cantidad_alimentos
        print(cantidad_alimentos, file=sys.stderr)
            
        valor = 0
        if cantidad_alimentos != None:
            valor = cantidad_alimentos / float(produccion.cantidad)
        resultado = ""
        if valor <= 0.83:
            resultado = "Excelente"
        elif valor <= 1:
            resultado = "Buena"
        elif valor <= 1.5:
            resultado = "Mala"
        else:
            resultado = "Pésima"    
        
        Calificacion.objects.create(
            produccion_id = produccion.id,
            fecha_calificacion = fecha_produccion,
            valor = valor,
            resultado = resultado
        )
        messages.success(request, "Registro agregado")
        return redirect("/produccion")
    
    return render(request, "produccion/add.html", { "vacas": vacas })

@login_required(login_url='/auth/login')
def delete(request, id):
    if request.method == "DELETE":
        Produccion.objects.filter(id = id).delete()
        return JsonResponse({ "status": True, 
                             "type": "success", 
                             "text": "El registro ha sido eliminado" })   
def ajaxallproduccion(request):
    producciones = Produccion.objects.all()
    sum_produccion = Produccion.objects.all().aggregate(Sum('cantidad'))    
    return render(request, "produccion/ajax_produccion.html", { "producciones": producciones, 'sum_produccion': sum_produccion }) 

def ajaxfilterproduccion(request):
    if request.method == "POST":
        vaca = request.POST.get("vaca")
        daterange = request.POST.get("daterange")
        
        if vaca != "" and daterange != "":
            format_str = '%d%m%Y'
            start_date = daterange.split("-")[0].strip().replace(".", "")
            end_date = daterange.split("-")[1].strip().replace(".", "")
            start_obj = datetime.strptime(start_date, format_str)
            end_obj = datetime.strptime(end_date, format_str)
            sum_produccion = Produccion.objects.filter(vaca_id=vaca, fecha_produccion__gte=start_obj, fecha_produccion__lte=end_obj) .aggregate(Sum('cantidad')) 
            producciones = Produccion.objects.filter(vaca_id=vaca, fecha_produccion__gte=start_obj, fecha_produccion__lte=end_obj) 

        elif vaca != "" and daterange == "":
            producciones = Produccion.objects.filter(vaca_id=vaca)
            sum_produccion = Produccion.objects.filter(vaca_id=vaca).aggregate(Sum('cantidad'))
        elif vaca =="" and daterange != "":
            format_str = '%d%m%Y'
            start_date = daterange.split("-")[0].strip().replace(".", "")
            end_date = daterange.split("-")[1].strip().replace(".", "")
            start_obj = datetime.strptime(start_date, format_str)
            end_obj = datetime.strptime(end_date, format_str)
            producciones = Produccion.objects.filter(fecha_produccion__gte=start_obj, fecha_produccion__lte=end_obj)
            sum_produccion = Produccion.objects.filter(fecha_produccion__gte=start_obj, fecha_produccion__lte=end_obj).aggregate(Sum('cantidad'))
        else:
            sum_produccion = Produccion.objects.all().aggregate(Sum('cantidad'))
            producciones = Produccion.objects.all()
        return render(request, "produccion/ajax_produccion.html", { "producciones": producciones, 'sum_produccion': sum_produccion }) 