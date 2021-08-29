from django.shortcuts import render, redirect
from .models import Pajuela
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login')
def home(request):
    pajuelas = Pajuela.objects.all()
    return render(request, "pajuelas/home.html", { "pajuelas": pajuelas })

@login_required(login_url='/auth/login')
def add(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        raza = request.POST["raza"]
        fecha_compra = request.POST["fecha_compra"]
        costo = request.POST["costo"]
        # estado = request.POST["estado"]
        pajuela = Pajuela.objects.create(
                            nombre = nombre,
                            raza = raza,
                            fecha_compra = fecha_compra,
                            costo = costo,
                            # estado = estado
                            )
        pajuela.usuario = request.user
        pajuela.save()
        
        messages.success(request, "Registro agregado")
        return redirect("/pajuelas")
    return render(request, "pajuelas/add.html")

@login_required(login_url='/auth/login')
def update(request, id):
    
    if not request.user.has_perm('pajuelas.change_pajuela'):
        return redirect("/pajuelas")    
    
    if request.method == "POST":
        nombre = request.POST["nombre"]
        raza = request.POST["raza"]
        fecha_compra = request.POST["fecha_compra"]
        costo = request.POST["costo"]
        # estado = request.POST["estado"]
        Pajuela.objects.filter(id = id).update(
                            nombre = nombre,
                            raza = raza,
                            fecha_compra = fecha_compra,
                            costo = costo,
                            # estado = estado,
                            usuario_id = request.user.id,
                            updated_at = datetime.now())
        messages.success(request, "Registro actualizado")
        return redirect("/pajuelas")
    pajuela = Pajuela.objects.get(id = id)
    return render(request, "pajuelas/update.html", { "pajuela": pajuela })

@login_required(login_url='/auth/login')
def delete(request, id):
    if request.method == "DELETE":
        Pajuela.objects.filter(id = id).delete()
        return JsonResponse({ "status": True, 
                             "type": "success", 
                             "text": "El registro ha sido eliminado" })    

    