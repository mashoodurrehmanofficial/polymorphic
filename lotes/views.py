from django.shortcuts import render, redirect
from .models import Lote
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login')
def home(request):
    lotes = Lote.objects.all()
    for lote in lotes:
        if int(lote.tiempo_uso.replace("días", "").strip()) >= 29:
            lote.status = "descanso ideal"
            
        else:
            lote.status = " Falta  " +  str(30 - int(lote.tiempo_uso.replace("días", "").strip())) +  "días"


    return render(request, "lotes/home.html", { "lotes": lotes })

@login_required(login_url='/auth/login')
def add(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        carga = request.POST["carga"]
        fecha_entrada = request.POST["fecha_entrada"]
        fecha_salida = request.POST["fecha_salida"]
        lote = Lote.objects.create(
                                nombre = nombre,
                                carga = carga,
                                fecha_entrada = fecha_entrada,
                                fecha_salida = None if fecha_salida == '' else fecha_salida
                            )
        lote.usuario = request.user
        lote.save()
        messages.success(request, "Registro agregado")
        return redirect("/lotes")
    return render(request, "lotes/add.html")

@login_required(login_url='/auth/login')
def update(request, id):
    
    if not request.user.has_perm('lote.change_lote'):
        return redirect("/lote")    
    
    if request.method == "POST":
        nombre = request.POST["nombre"]
        carga = request.POST["carga"]
        fecha_entrada = request.POST["fecha_entrada"]
        fecha_salida = request.POST["fecha_salida"]
        lote = Lote.objects.filter(id = id).update(
                            nombre = nombre,
                            carga = carga,
                            fecha_entrada = fecha_entrada,
                            fecha_salida = None if fecha_salida == '' else fecha_salida,
                            usuario_id = request.user.id,
                            updated_at = datetime.now())
        
        messages.success(request, "Registro actualizado")
        return redirect("/lotes")
    lote = Lote.objects.get(id = id)
    return render(request, "lotes/update.html", { "lote": lote })

@login_required(login_url='/auth/login')
def delete(request, id):
    if request.method == "DELETE":
        Lote.objects.filter(id = id).delete()
        return JsonResponse({ "status": True, 
                             "type": "success", 
                             "text": "El registro ha sido eliminado" })    

    