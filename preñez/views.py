from django.shortcuts import render, redirect
from .models import Preñez
from vacas.models import Vaca, BornHistory
from toros.models import Toro
from pajuelas.models import Pajuela
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
import sys
from django.contrib.auth.decorators import login_required
import dateutil.parser
from datetime import date
from crias.models import Cria

@login_required(login_url='/auth/login')
def home(request):
    fecundaciones = Preñez.objects.all()
    return render(request, "prenez/home.html", { "fecundaciones": fecundaciones })

@login_required(login_url='/auth/login')
def add(request):
    if request.method == "POST":
        fecha_preñez = request.POST["fecha_preñez"]
        metodo = request.POST["metodo"]
        metodo_id = request.POST["metodo_id"]
        preñez = Preñez.objects.create(
                                vaca_id = request.POST["vaca_id"],
                                fecha_preñez = fecha_preñez
                            )
        preñez.usuario = request.user
        preñez.save()
        if metodo == "toro":
            toro = Toro.objects.get(id = metodo_id)
            toro.fecundaciones.add(preñez)
            
        if metodo == "pajuela":
            pajuela = Pajuela.objects.get(id = metodo_id)
            pajuela.fecundaciones.add(preñez)
            
        messages.success(request, "Registro agregado")
        return redirect("/preñez")
    
    vaca_arr = []
    b_vaca_arr = []
    bn_vaca_arr = []
    today = date.today()
    a_month = dateutil.relativedelta.relativedelta(months = 16)
    a_date = dateutil.relativedelta.relativedelta(days = 45)

    fecha_menos = today - a_month
    cria_date = today - a_date
    prez_id  = [x.vaca_id for x in Preñez.objects.all()]
    print("----------dd------------", fecha_menos)
    born_id = [x.vaca_id for x in BornHistory.objects.all()]
    b_vacas = Vaca.objects.filter(id__in=born_id, fecha_nacimiento__lte=fecha_menos).exclude(id__in=prez_id)
    bn_vacas = Vaca.objects.filter(fecha_nacimiento__lte=fecha_menos).exclude(id__in=born_id).exclude(id__in=prez_id)
    print("------", b_vacas)
    for b_vaca in b_vacas:
        h_vaca = BornHistory.objects.get(vaca_id=b_vaca.id)
        if h_vaca.fecha < cria_date:
            b_vaca_arr.append(b_vaca)
    for bn_vaca in bn_vacas:
        bn_vaca_arr.append(bn_vaca)

    vaca_arr.extend(b_vaca_arr)
    vaca_arr.extend(bn_vaca_arr)

    return render(request, "prenez/add.html", { "vacas": vaca_arr })

@login_required(login_url='/auth/login')
def update(request, id):
    
    if not request.user.has_perm('preñez.change_preñez'):
        return redirect("/preñez")    
    
    if request.method == "POST":
        fecha_preñez = request.POST["fecha_preñez"]
        metodo = request.POST["metodo"]
        metodo_id = request.POST["metodo_id"]
        Preñez.objects.filter(id = id).update(
                            vaca_id = request.POST["vaca_id"],
                            fecha_preñez = fecha_preñez,
                            usuario_id = request.user.id,
                            updated_at = datetime.now())
        messages.success(request, "Registro actualizado")
        return redirect("/preñez")
    preñez = Preñez.objects.get(id = id)
    seleccion = preñez.fecundaciones.all()[0]
    preñez.metodo = seleccion.__class__.__name__;
    preñez.seleccion_id = seleccion.id
    selecciones = []
    if preñez.metodo == "Toro":
        selecciones = Toro.objects.all()        
    else:
        selecciones = Pajuela.objects.all()
        
    vaca_arr = []
    b_vaca_arr = []
    bn_vaca_arr = []
    today = date.today()
    a_month = dateutil.relativedelta.relativedelta(months = 16)
    a_date = dateutil.relativedelta.relativedelta(days = 45)

    fecha_menos = today - a_month
    cria_date = today - a_date
    prez_id  = [x.vaca_id for x in Preñez.objects.all().exclude(id=id)]
    born_id = [x.vaca_id for x in BornHistory.objects.all()]
    b_vacas = Vaca.objects.filter(id__in=born_id, fecha_nacimiento__lte=fecha_menos).exclude(id__in=prez_id)
    bn_vacas = Vaca.objects.filter(fecha_nacimiento__lte=fecha_menos).exclude(id__in=born_id).exclude(id__in=prez_id)

    for b_vaca in b_vacas:
        h_vaca = BornHistory.objects.get(vaca_id=b_vaca.id)
        if h_vaca.fecha < cria_date:
            b_vaca_arr.append(b_vaca)
    for bn_vaca in bn_vacas:
        bn_vaca_arr.append(bn_vaca)

    vaca_arr.extend(b_vaca_arr)
    vaca_arr.extend(bn_vaca_arr)
    
    return render(request, "prenez/update.html", { "vacas": vaca_arr, "preñez": preñez, "selecciones": selecciones })

@login_required(login_url='/auth/login')
def delete(request, id):
    if request.method == "DELETE":
        Preñez.objects.filter(id = id).delete()
        return JsonResponse({ "status": True, 
                             "type": "success", 
                             "text": "El registro ha sido eliminado" })    

@login_required(login_url='/auth/login')
def getToros(request):
    toros = Toro.objects.filter(estado = "Activo")
    t = []
    for toro in toros:
        t.append({"id": toro.id, "nombre": toro.nombre})
    return JsonResponse(t, safe = False)

@login_required(login_url='/auth/login')
def getPajuelas(request):
    pajuelas_id = [x.id for x in Pajuela.objects.all() if x.dias_compra < 90]
    pajuelas = Pajuela.objects.filter(id__in = pajuelas_id)
    p = []
    for pajuela in pajuelas:
        p.append({"id": pajuela.id, "nombre": pajuela.nombre})
    return JsonResponse(p, safe = False)

