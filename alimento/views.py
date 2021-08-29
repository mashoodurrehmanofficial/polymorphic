from django.shortcuts import render, redirect
from .models import Alimento, AlimentoExport
from vacas.models import Vaca
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import datetime
from decimal import Decimal
from django.db.models import Sum

@login_required(login_url='/auth/login')
def home(request):
    alimentos = Alimento.objects.all()
    sum_alimento = Alimento.objects.values('nombre').annotate(Sum('cantidad'))
    all_data = Alimento.objects.all().aggregate(Sum('cantidad'))
    arr_name = []
    arr_cantidad = []
    for s_alimento in sum_alimento:
        arr_name.append(s_alimento['nombre'])
        arr_cantidad.append(int(float(s_alimento['cantidad__sum'])))
    arr_name.append('Todo')
    arr_cantidad.append(int(float(all_data['cantidad__sum'])))
    return render(request, "alimento/home.html",{ "alimentos": alimentos, 'g_name': arr_name,'g_cantidad': arr_cantidad  })

@login_required(login_url='/auth/login')
def export(request):
    alimentosexport = AlimentoExport.objects.all()
    sum_alimentoexport = AlimentoExport.objects.values('nombre').annotate(Sum('cantidad'))
    all_data = AlimentoExport.objects.all().aggregate(Sum('cantidad'))
    arr_name = []
    arr_cantidad = []
    for s_alimento in sum_alimentoexport:
        arr_name.append(s_alimento['nombre'])
        arr_cantidad.append(int(float(s_alimento['cantidad__sum'])))
    arr_name.append('Todo')
    arr_cantidad.append(int(float(all_data['cantidad__sum'])))

    return render(request, "alimento/export.html",{ "alimentosexport": alimentosexport, 'g_name': arr_name,'g_cantidad': arr_cantidad  })

@login_required(login_url='/auth/login')
def add(request):
    if request.method == "POST":
        # vaca_id = request.POST["vaca_id"]
        nombre = request.POST["nombre"]
        cantidad = request.POST["cantidad"]
        costo = request.POST["costo"]
        fecha_suministro = request.POST["fecha_suministro"]
        alimento = Alimento.objects.create(
                                # vaca_id = vaca_id,
                                nombre = nombre,
                                cantidad = cantidad,
                                costo = costo,
                                fecha_suministro = fecha_suministro
                            )
        alimento.usuario = request.user
        alimento.save()
        messages.success(request, "Registro agregado")
        return redirect("/alimento")
    vacas = Vaca.objects.all()
    return render(request, "alimento/add.html", { "vacas": vacas })

@login_required(login_url='/auth/login')
def update(request, id):
    
    if not request.user.has_perm('alimento.change_alimento'):
        return redirect("/alimento")    
    
    if request.method == "POST":
        # vaca_id = request.POST["vaca_id"]
        nombre = request.POST["nombre"]
        cantidad = request.POST["cantidad"]
        costo = request.POST["costo"]
        fecha_suministro = request.POST["fecha_suministro"]
        alimento = Alimento.objects.filter(id = id).update(
                            # vaca_id = vaca_id,
                            nombre = nombre,
                            cantidad = Decimal(cantidad.replace(',','.')),
                            costo = Decimal(costo.replace(',','.')),
                            fecha_suministro = fecha_suministro,
                            usuario_id = request.user.id,
                            updated_at = datetime.datetime.now())
        
        messages.success(request, "Registro actualizado")
        return redirect("/alimento")
    alimento = Alimento.objects.get(id = id)
    vacas = Vaca.objects.all()
    return render(request, "alimento/update.html", { "vacas": vacas, "alimento": alimento })

@login_required(login_url='/auth/login')
def delete(request, id):
    if request.method == "DELETE":
        Alimento.objects.filter(id = id).delete()
        return JsonResponse({ "status": True, 
                             "type": "success", 
                             "text": "El registro ha sido eliminado" })    

def ajaxallalimento(request):
    if request.method == "POST":
        alimentos = Alimento.objects.all()
        return render(request, "alimento/ajax_alimento.html", { "alimentos": alimentos })

def ajaxfilteralimento(request):

    if request.method == "POST":
        name = request.POST.get("name")
        daterange = request.POST.get("daterange")

        if name != "" and daterange != "":

            format_str = '%d%m%Y'
            start_date = daterange.split("-")[0].strip().replace(".", "")
            end_date = daterange.split("-")[1].strip().replace(".", "")
            start_obj = datetime.datetime.strptime(start_date, format_str)
            end_obj = datetime.datetime.strptime(end_date, format_str)
            alimentos = Alimento.objects.filter(nombre__contains=name, fecha_suministro__gte=start_obj, fecha_suministro__lte=end_obj)
        elif name != "" and daterange == "":
            alimentos = Alimento.objects.filter(nombre__contains=name)
        elif name == "" and daterange != "":
            
            format_str = '%d%m%Y'
            start_date = daterange.split("-")[0].strip().replace(".", "")
            end_date = daterange.split("-")[1].strip().replace(".", "")
            start_obj = datetime.datetime.strptime(start_date, format_str)
            end_obj = datetime.datetime.strptime(end_date, format_str)
            alimentos = Alimento.objects.filter(fecha_suministro__gte=start_obj, fecha_suministro__lte=end_obj)

        else:
            alimentos = Alimento.objects.all()

        return render(request, "alimento/ajax_alimento.html", { "alimentos": alimentos })

def ajaxgetalimento(request):
    if request.method == "POST":

        alimento_id = request.POST.get("alimento_id")
        alimento = Alimento.objects.get(id=alimento_id)

        return JsonResponse({"o_quantity": alimento.cantidad, "name": alimento.nombre })   

def ajaxalimentoexport(request):
    if request.method == "POST":
        alimentoid = request.POST.get('alimento_id')
        cantidad = request.POST.get('cantidad')

        destino = request.POST.get('destino')
        usedate = request.POST.get('usedate')
        name = request.POST.get('name')

        AlimentoExport.objects.create(
            nombre=name,
            cantidad=cantidad,
            destino=destino,
            fecha_export=usedate,
            alimento_id=alimentoid,

        )
        alimento = Alimento.objects.get(id=alimentoid)
        alimento.cantidad = alimento.cantidad - Decimal(cantidad)
        alimento.save()

        return JsonResponse({"status": "OK" })  








    