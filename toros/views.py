from django.shortcuts import render, redirect
from .models import Toro
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from datetime import date
from django.core.files.storage import default_storage
import shutil
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required(login_url='/auth/login')
def home(request):
    toros = Toro.objects.all().exclude(~Q(processm=None))
    current_time = date.today()
    return render(request, "toros/home.html", { "toros": toros, "current_time" : current_time })

@login_required(login_url='/auth/login')
def add(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        raza = request.POST["raza"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]
        fecha_compra = request.POST["fecha_compra"]
        fecha_primer_monta = request.POST["fecha_primer_monta"]
        costo = request.POST["costo"]
        estado = request.POST["estado"]
        motivo_estado = request.POST["motivo_estado"]
        file = request.FILES['foto'] if len(request.FILES) != 0 else None
        
        
        if datetime.strptime(fecha_compra, "%Y-%m-%d") < datetime.strptime(fecha_nacimiento, "%Y-%m-%d"):
            messages.error(request, "La fecha de compra no puede ser menor a la de fecha de nacimiento")
            return render(request, "toros/add.html")        
        
        if datetime.strptime(fecha_primer_monta, "%Y-%m-%d") < datetime.strptime(fecha_compra, "%Y-%m-%d"):
            messages.error(request, "La fecha de primer monta no puede ser menor a la de fecha de compra")
            return render(request, "toros/add.html")     
        
        otro_toro = Toro.objects.filter(nombre = nombre).first()
        
        if otro_toro is not None:
            messages.error(request, "Ya existe otro toro con el nombre ingresado")
            return render(request, "toros/add.html")   
        
        toro = Toro.objects.create(nombre = nombre,
                            raza = raza,
                            fecha_nacimiento = fecha_nacimiento,
                            fecha_compra = fecha_compra,
                            fecha_primer_monta = fecha_primer_monta,
                            costo = costo,
                            estado = estado,
                            foto = file.name if file is not None else None,
                            motivo_estado = motivo_estado)
        toro.usuario = request.user
        toro.save()
        if len(request.FILES) != 0:
            file_name = default_storage.save("static/uploads/toros/" + str(toro.id) + "/" + file.name, file)
        messages.success(request, "Registro agregado")
        return redirect("/toros")
    return render(request, "toros/add.html")

@login_required(login_url='/auth/login')
def update(request, id):
    
    if not request.user.has_perm('toros.change_toro'):
        return redirect("/toros")
    
    if request.method == "POST":
        nombre = request.POST["nombre"]
        raza = request.POST["raza"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]
        fecha_compra = request.POST["fecha_compra"]
        fecha_primer_monta = request.POST["fecha_primer_monta"]
        # edad = request.POST["edad"]
        estado = request.POST["estado"]
        motivo_estado = "" if estado == "Activo" else request.POST["motivo_estado"]
        
        if len(request.FILES) != 0:
            file = request.FILES['foto']
        
        if datetime.strptime(fecha_compra, "%Y-%m-%d") < datetime.strptime(fecha_nacimiento, "%Y-%m-%d"):
            messages.error(request, "La fecha de compra no puede ser menor a la de fecha de nacimiento")
            return render(request, "toros/add.html")        
        
        if datetime.strptime(fecha_primer_monta, "%Y-%m-%d") < datetime.strptime(fecha_compra, "%Y-%m-%d"):
            messages.error(request, "La fecha de primer monta no puede ser menor a la de fecha de compra")
            return render(request, "toros/add.html")      
        
        otro_toro = Toro.objects.filter(nombre = nombre).exclude(id = id).first()
        
        if otro_toro is not None:
            messages.error(request, "Ya existe otro toro con el nombre ingresado")
            return redirect("/toros/update/" + str(id))  
            
        toro = Toro.objects.get(id = id)
        toro.nombre = nombre
        toro.raza = raza
        toro.fecha_nacimiento = fecha_nacimiento
        toro.fecha_compra = fecha_compra
        toro.fecha_primer_monta = fecha_primer_monta
        toro.estado = estado
        toro.motivo_estado = motivo_estado
        if len(request.FILES) != 0:
            toro.foto = file.name
        if request.POST['foto_old'] == "":
            toro.foto = None
        toro.usuario = request.user
        toro.save()
        
        # Toro.objects.filter(id = id).update(nombre = nombre,
        #                     raza = raza,
        #                     fecha_nacimiento = fecha_nacimiento,
        #                     fecha_compra = fecha_compra,
        #                     fecha_primer_monta = fecha_primer_monta,
        #                     # edad = edad,
        #                     estado = estado,
        #                     motivo_estado = motivo_estado,
        #                     updated_at = datetime.now())
        
        path = "static/uploads/toros/" + str(toro.id) + "/"
        if (len(request.FILES) != 0 or request.POST['foto_old'] == '') and default_storage.exists(path):
            shutil.rmtree(path)
        if len(request.FILES) != 0:            
            file_name = default_storage.save(path + file.name, file)
        
        messages.success(request, "Registro actualizado")
        return redirect("/toros")
    toro = Toro.objects.get(id = id)
    return render(request, "toros/update.html", { "toro": toro })

@login_required(login_url='/auth/login')
def delete(request, id):
    if request.method == "DELETE":
        Toro.objects.filter(id = id).delete()
        return JsonResponse({ "status": True, 
                             "type": "success", 
                             "text": "El registro ha sido eliminado" })    

def ajaxprocesstoro(request):
    if request.method == "POST":
        toro_id = request.POST['toro_id']
        processm = request.POST['processm']
        reason = request.POST['reason']
        fecha_processm = request.POST['fecha_processm']

        toro = Toro.objects.get(id=toro_id)

        toro.processm = processm
        toro.fecha_processm = fecha_processm
        toro.reason = reason

        toro.save()

        return JsonResponse({ "status": "OK"})

    