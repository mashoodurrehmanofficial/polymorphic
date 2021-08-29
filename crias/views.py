from django.shortcuts import render, redirect
from .models import Cria
from vacas.models import Vaca, BornHistory, Raza
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from datetime import date
from django.contrib.auth.decorators import login_required
import dateutil.parser
from preñez.models import Preñez
from django.http import HttpResponseRedirect

@login_required(login_url='/auth/login')
def home(request):
    crias = Cria.objects.filter(nacimiento="Vivo")
    current_time = date.today()
    return render(request, "crias/home.html", { "crias": crias, "current_time" : current_time })

@login_required(login_url='/auth/login')
def add(request):
    vacas_id = [x.vaca_id for x in Preñez.objects.all()]
    print("---------", vacas_id)
    
    vacas = Vaca.objects.filter(id__in=vacas_id)
    print("-------", Vaca.objects.all())
    
    if request.method == "POST":
        vaca_id = request.POST["vaca_id"]
        nombre = request.POST["nombre"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]
        sexo = request.POST["sexo"]
        nacimiento = request.POST["nacimiento"]
        destino = request.POST["destino"]
        raza = request.POST["raza"]

               
        # buscamos las crias que estén registradas en menos de 9 meses, antes o después de la fecha de nacimiento indicada 
        if nacimiento !="Muerto":
            prez = Preñez.objects.get(vaca_id=vaca_id)
            fecha_nacimiento_x = datetime.strptime(fecha_nacimiento, "%Y-%m-%d") 
            a_month = dateutil.relativedelta.relativedelta(months = 7)

            if prez.fecha_preñez > datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date() -a_month:
                messages.error(request, "Fecha de nacimiento no válida")
                return render(request, "crias/add.html", { "vacas": vacas }) 

            
            a_month = dateutil.relativedelta.relativedelta(months = 9)
            fecha_menos = fecha_nacimiento_x - a_month
            fecha_mas = fecha_nacimiento_x + a_month
            crias = Cria.objects.filter(fecha_nacimiento__gte = fecha_menos, fecha_nacimiento__lte = fecha_nacimiento) | Cria.objects.filter(fecha_nacimiento__gte = fecha_nacimiento, fecha_nacimiento__lte = fecha_mas)
            
            if crias.count() > 0:
                messages.error(request, "Fecha de nacimiento no válida")
                return render(request, "crias/add.html", { "vacas": vacas })

        else:
            prez = Preñez.objects.get(vaca_id=vaca_id)
            if prez.fecha_preñez > datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date():
                messages.error(request, "Fecha de nacimiento no válida")
                return render(request, "crias/add.html", { "vacas": vacas })
        
        vaca = Vaca.objects.get(id = vaca_id)
        
        if vaca.tiempo_preñez is None:
            messages.error(request, "La vaca elegida no ha estado en preñez")
            return render(request, "crias/add.html", { "vacas": vacas })
        
        # if vaca.preñez_pasada == True:
        #     messages.error(request, "Preñez muy avanzada")
        #     return render(request, "crias/add.html", { "vacas": vacas })
        
        otra_cria = Cria.objects.filter(nombre = nombre).first()
        
        if otra_cria is not None:
            messages.error(request, "Ya existe otra cria con el nombre ingresado")
            return render(request, "crias/add.html")
        
        cria = Cria.objects.create(
                            vaca_id = vaca_id,
                            nombre = nombre,
                            fecha_nacimiento = fecha_nacimiento,
                            sexo = sexo,
                            nacimiento = nacimiento,
                            destino = destino,
                            raza=raza
                            )
        cria.usuario = request.user
        cria.save()
        prez =  Preñez.objects.filter(vaca_id=vaca_id).first()
        prez.delete()
        if BornHistory.objects.filter(vaca_id=vaca_id).exists():
            born = BornHistory.objects.get(vaca_id=vaca_id)
            born.fecha = fecha_nacimiento
            born.save()
        else:
            BornHistory.objects.create(
                vaca_id=vaca_id,
                fecha=fecha_nacimiento
            )
        messages.success(request, "Registro agregado")
        return redirect("/crias")
    razas = Raza.objects.all()
    return render(request, "crias/add.html", { "vacas": vacas, 'razas': razas })

@login_required(login_url='/auth/login')
def update(request, id):
    
    if not request.user.has_perm('crias.change_cria'):
        return redirect("/crias")    
    
    if request.method == "POST":
        vaca_id = request.POST["vaca_id"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]
        nombre = request.POST["nombre"]
        sexo = request.POST["sexo"]
        nacimiento = request.POST["nacimiento"]
        destino = request.POST["destino"]
        raza = request.POST["raza"]
        
        otra_cria = Cria.objects.filter(nombre = nombre).exclude(id = id).first()
        
        if otra_cria is not None:
            messages.error(request, "Ya existe otra cria con el nombre ingresado")
            return redirect("/crias/update/" + str(id))
        
        cria = Cria.objects.get(id = id)
        cria.vaca_id = vaca_id
        cria.fecha_nacimiento = fecha_nacimiento
        cria.nombre = nombre
        cria.sexo = sexo
        cria.nacimiento = nacimiento
        cria.destino = destino
        cria.usuario_id = request.user.id
        cria.raza = raza
        cria.save()
        
        if "pasar_vaca" in request.POST:
            vaca = Vaca.objects.create(
                            nombre = cria.nombre,
                            raza = '',
                            fecha_nacimiento = cria.fecha_nacimiento,
                            foto = None
                            )            
            Cria.objects.filter(id = id).update(vaca_madura_id = vaca.id)
        
        messages.success(request, "Registro actualizado")
        return redirect("/crias")
    cria = Cria.objects.get(id = id)
    vacas = Vaca.objects.all()
    return render(request, "crias/update.html", { "vacas": vacas, "cria": cria })

@login_required(login_url='/auth/login')
def delete(request, id):
    if request.method == "DELETE":
        Cria.objects.filter(id = id).delete()
        return JsonResponse({ "status": True, 
                             "type": "success", 
                             "text": "El registro ha sido eliminado" })  



def ajax_date_check(request):
    if request.method == "POST":
        fecha = request.POST.get("fecha") 
        vaca_id=request.POST.get("vaca_id")

        a_month = dateutil.relativedelta.relativedelta(months = 7)
        final = datetime.strptime(fecha, '%Y-%m-%d').date() - a_month

        prez = Preñez.objects.get(vaca_id=int(vaca_id))

        if prez.fecha_preñez < final:
            return JsonResponse({ "status": "NO", 
                            })
        else:
            return JsonResponse({ "status": "OK", 
                            })



    