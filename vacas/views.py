from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Vaca, Raza
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from datetime import date
from django.core.files.storage import default_storage
import shutil
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url='/auth/login')
def home(request):
    vacas = Vaca.objects.all()
    current_time = date.today()
    
    return render(request, "vacas/home.html", { "current_time" : current_time, 'vacas': vacas })

def ajax_raza_add(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        if Raza.objects.filter(nombre__iexact=nombre).exists():
           return JsonResponse({
                "status": "Existed"
            }) 
        else:
            Raza.objects.create(
                nombre=nombre
            )

            return JsonResponse({
                "status": "Success"
            })

@login_required(login_url='/auth/login')
def add(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]

        raza = request.POST["raza"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]
        # edad = request.POST["edad"]
        # tiempo_preñez = request.POST["tiempo_preñez"]        
        file = request.FILES['foto'] if len(request.FILES) != 0 else None
        
        otra_vaca = Vaca.objects.filter(nombre = nombre).first()
        
        if otra_vaca is not None:
            messages.error(request, "Ya existe otra vaca con el nombre ingresado")
            return render(request, "vacas/add.html")
 
        vaca = Vaca.objects.create(nombre = nombre,
                            raza = raza,
                            fecha_nacimiento = fecha_nacimiento,
                            # edad = edad,
                            # tiempo_preñez = tiempo_preñez,
                            foto = file.name if file is not None else None
                            )
        
        vaca.usuario = request.user
        vaca.save()
        
        if len(request.FILES) != 0:
            file_name = default_storage.save("static/uploads/vacas/" + str(vaca.id) + "/" + file.name, file)
        messages.success(request, "Registro agregado")
        return redirect("/vacas")
    razas = Raza.objects.all()
    return render(request, "vacas/add.html", {'razas': razas})

@login_required(login_url='/auth/login')
def update(request, id = None):
    
    if not request.user.has_perm('vacas.change_vaca'):
        return redirect("/vacas")
    
    if request.method == "POST":
        nombre = request.POST["nombre"]
        raza = request.POST["raza"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]
        # edad = request.POST["edad"]
        # tiempo_preñez = request.POST["tiempo_preñez"]

        if len(request.FILES) != 0:
            file = request.FILES['foto']
            
        otra_vaca = Vaca.objects.filter(nombre = nombre).exclude(id = id).first()
        
        if otra_vaca is not None:
            messages.error(request, "Ya existe otra vaca con el nombre ingresado")
            return redirect("/vacas/update/" + str(id))
            
        vaca = Vaca.objects.get(id = id)
        vaca.nombre = nombre
        vaca.raza = raza

        vaca.fecha_nacimiento = fecha_nacimiento
        # vaca.tiempo_preñez = tiempo_preñez
        if len(request.FILES) != 0:
            vaca.foto = file.name
        if request.POST['foto_old'] == "":
            vaca.foto = None
        
        vaca.usuario = request.user
        vaca.save()
        # Vaca.objects.filter(id = id).update(nombre = nombre,
        #                     raza = raza,
        #                     fecha_nacimiento = fecha_nacimiento,
        #                     # edad = edad,
        #                     tiempo_preñez = tiempo_preñez,
        #                     foto = file.name,
        #                     updated_at = datetime.now())
        
        path = "static/uploads/vacas/" + str(vaca.id) + "/"
        if (len(request.FILES) != 0 or request.POST['foto_old'] == '') and default_storage.exists(path):
            shutil.rmtree(path)
        if len(request.FILES) != 0:            
            file_name = default_storage.save(path + file.name, file)
        # messages.success(request, "Registro agregado" if a == None else "Registro actualizado")
        messages.success(request, "Registro actualizado")
        return redirect("/vacas")
    vaca = Vaca.objects.get(id = id)
    return render(request, "vacas/update.html", { "vaca": vaca })

@login_required(login_url='/auth/login')
def delete(request, id):
    
    if not request.user.has_perm('vacas.delete_vaca'):
        return redirect("/vacas")    
    
    if request.method == "DELETE":
        
        vaca = Vaca.objects.get(id = id)
        
        path = "static/uploads/vacas/" + str(vaca.id) + "/"
        if default_storage.exists(path):
            shutil.rmtree(path)
        
        vaca.delete()
        
        return JsonResponse({ "status": True, 
                             "type": "success", 
                             "text": "El registro ha sido eliminado" })    

def ajaxallvacas(request):
    if request.method == "POST":
        vacas = Vaca.objects.all().exclude(~Q(processm=None))
        current_time = date.today()

        return render(request, 'vacas/ajax_vacas.html', {'vacas': vacas, "current_time" : current_time })


def ajaxprocessvacas(request):
    if request.method == "POST":
        vacas_id = request.POST['vacas_id']
        processm = request.POST['processm']
        reason = request.POST['reason']
        fecha_processm = request.POST['fecha_processm']

        vacas = Vaca.objects.get(id=vacas_id)

        vacas.processm = processm
        vacas.fecha_processm = fecha_processm
        vacas.reason = reason

        vacas.save()

        return HttpResponse("OK")


def ajaxfiltervacas(request):
    if request.method == "POST":
        current_time = date.today()
        razas = request.POST.get("razas")
        name = request.POST.get("name")
        daterange = request.POST.get("daterange")
        if razas != "" and name == "" and daterange == "":
            
            vacas = Vaca.objects.filter(raza__contains=razas).exclude(~Q(processm=None))

        elif razas != "" and name != "" and daterange == "":
            vacas = Vaca.objects.filter(nombre__contains=name, raza__contains=razas).exclude(~Q(processm=None))

        elif razas != "" and name != "" and daterange != "":
            format_str = '%d%m%Y'
            start_date = daterange.split("-")[0].strip().replace(".", "")
            end_date = daterange.split("-")[1].strip().replace(".", "")
            start_obj = datetime.datetime.strptime(start_date, format_str)
            end_obj = datetime.datetime.strptime(end_date, format_str)

            vacas = Vaca.objects.filter(raza__contains=razas,nombre__contains=name, updated_at__gte=start_obj, updated_at__lte=end_obj).exclude(~Q(processm=None))
        elif razas == "" and name != "" and daterange == "":

            vacas = Vaca.objects.filter(nombre__contains=name).exclude(~Q(processm=None))

        elif razas == "" and name != "" and daterange != "":
            format_str = '%d%m%Y'
            start_date = daterange.split("-")[0].strip().replace(".", "")
            end_date = daterange.split("-")[1].strip().replace(".", "")
            start_obj = datetime.datetime.strptime(start_date, format_str)
            end_obj = datetime.datetime.strptime(end_date, format_str)
            vacas = Vaca.objects.filter(nombre__contains=name,updated_at__gte=start_obj, updated_at__lte=end_obj).exclude(~Q(processm=None))
        elif razas != "" and name == "" and daterange != "":
            format_str = '%d%m%Y'
            start_date = daterange.split("-")[0].strip().replace(".", "")
            end_date = daterange.split("-")[1].strip().replace(".", "")
            start_obj = datetime.datetime.strptime(start_date, format_str)
            end_obj = datetime.datetime.strptime(end_date, format_str)
            vacas = Vaca.objects.filter(raza__contains=razas,updated_at__gte=start_obj, updated_at__lte=end_obj).exclude(~Q(processm=None))

        elif razas == "" and name == "" and daterange != "":
            format_str = '%d%m%Y'
            start_date = daterange.split("-")[0].strip().replace(".", "")
            end_date = daterange.split("-")[1].strip().replace(".", "")
            start_obj = datetime.datetime.strptime(start_date, format_str)
            end_obj = datetime.datetime.strptime(end_date, format_str)

            vacas = Vaca.objects.filter(raza__contains=razas, updated_at__gte=start_obj, updated_at__lte=end_obj).exclude(~Q(processm=None))
        else:
            vacas = Vaca.objects.all().exclude(~Q(processm=None))
        
        return render(request, 'vacas/ajax_vacas.html', {'vacas': vacas, "current_time" : current_time })


    