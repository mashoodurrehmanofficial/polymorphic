from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from vacas.models import Vaca
from toros.models import Toro
from usuarios.models import UsuarioInfo
from pajuelas.models import Pajuela
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
import sys
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
import shutil
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from usuarios.email import send_mail
from authx.models import ValidateCode
# import threading
import random
import math


# from django.conf import settings
# from django.core.mail import send_mail

@login_required(login_url='/auth/login')
def home(request):
    
    if not request.user.has_perm('usuarios.view_usuario'):
        return redirect("/")
    
    usuarios = User.objects.all()
    for u in usuarios:
        u.rol = u.groups.all()[0].name
        
    return render(request, "usuarios/home.html", { "usuarios": usuarios })

@login_required(login_url='/auth/login')
def add(request):
    
    # if not request.user.has_perm('usuarios.add_usuario'):
    #     return redirect("/")
    
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = make_password(request.POST["password"])
        rol = request.POST["rol"]
        random_str = request.POST['code']
        file = request.FILES['foto'] if len(request.FILES) != 0 else None
        usuario = User.objects.create(
                                first_name = first_name,
                                last_name = last_name,
                                email = email,
                                username = username,
                                password = password,
                                is_active = False,
                            )

        
        UsuarioInfo.objects.create(
            usuario_id = usuario.id,
            foto = file.name if file is not None else None
        )

        ValidateCode.objects.create(
            user_id = usuario.id,
            code=random_str 
        )
        mail_subject = "¡Bienvenido a nuestro sitio!"
        mail_context = {
                    'email_title': "¡Bienvenido a nuestro sitio!",
                    'email_body': "Utiliza este email para activar tu cuenta, y empezar a trabajar con nuestra plataforma.",
                    'user': usuario,
                    'site_url': request._current_scheme_host,
                    'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
                    'token': default_token_generator.make_token(usuario),
                    'key_Code': random_str,
                }
        send_mail(mail_subject, email_template_name=None,
                                context=mail_context, to_email=[usuario.email],
                                html_email_template_name='usuarios/register_email.html')
        
        if len(request.FILES) != 0:
            file_name = default_storage.save("static/uploads/usuarios/" + str(usuario.id) + "/" + file.name, file)
        
        if rol == "admin":
            my_group = Group.objects.get(name='Administradores') 
            my_group.user_set.add(usuario)
        else:
            my_group = Group.objects.get(name='Obreros') 
            my_group.user_set.add(usuario)
            
        messages.success(request, "Registro agregado")
        return redirect("/usuarios")
    return render(request, "usuarios/add.html")

def generateCode(request):
    if request.method == "POST":

        ## storing strings in a list
        digits = [i for i in range(0, 10)]

        ## initializing a string
        random_str = ""

        ## we can generate any lenght of string we want
        for i in range(6):
            index = math.floor(random.random() * 10)
            random_str += str(digits[index])

        return JsonResponse({"code": random_str})


@login_required(login_url='/auth/login')
def update(request, id):
    
    if not request.user.has_perm('usuarios.change_usuario'):
        return redirect("/")
    
    if request.method == "POST":
        
        usuario = User.objects.get(id = id)
        usuarioInfo = UsuarioInfo.objects.filter(usuario_id = usuario.id).first()
        
        if usuarioInfo is None:
            usuarioInfo = UsuarioInfo.objects.create(
                usuario_id = usuario.id,
                foto = None
            )
        
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        
        if usuario.password != request.POST["password"]:
            password = make_password(request.POST["password"])
        else:
            password = usuario.password    
            
        if len(request.FILES) != 0:
            file = request.FILES['foto']                            
                
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.email = email
        usuario.username = username
        usuario.password = password
        
        if len(request.FILES) != 0:
            usuarioInfo.foto = file.name
        if request.POST['foto_old'] == "":
            usuarioInfo.foto = None            
        
        usuario.save()
        usuarioInfo.save()
        
        path = "static/uploads/usuarios/" + str(usuario.id) + "/"
        if (len(request.FILES) != 0 or request.POST['foto_old'] == '') and default_storage.exists(path):
            shutil.rmtree(path)
        if len(request.FILES) != 0:            
            file_name = default_storage.save(path + file.name, file)
        
        rol = request.POST["rol"]
        
        if usuario.groups.all()[0].name == "Obreros" and rol == "admin":            
            my_group = Group.objects.get(name='Obreros') 
            my_group.user_set.remove(usuario)
            my_group = Group.objects.get(name='Administradores') 
            my_group.user_set.add(usuario)
            
        if usuario.groups.all()[0].name == "Administradores" and rol == "obrero":            
            my_group = Group.objects.get(name='Administradores') 
            my_group.user_set.remove(usuario)
            my_group = Group.objects.get(name='Obreros') 
            my_group.user_set.add(usuario)
            
        # usuario_pass = "usuario123"
        # usuario_pass_hashed = make_password(usuario_pass)
            
        # send_mail(
        #     'Recuperación de contraseña',
        #     'Hola, este correo es enviado desde un post en PyWombat. 🐍',
        #     settings.EMAIL_HOST_USER,
        #     ['xscorpio_@hotmail.com'],
        #     fail_silently=False
        # )
        
        messages.success(request, "Registro actualizado")
        return redirect("/usuarios")
    
    usuario = User.objects.get(id = id)
    usuario.rol = usuario.groups.all()[0].name
    
    return render(request, "usuarios/update.html", { "usuario": usuario })

@login_required(login_url='/auth/login')
def delete(request, id):
    if request.method == "DELETE":
        
        usuario = User.objects.get(id = id)
        
        if request.user.id == id:
            return JsonResponse({ "status": False, 
                             "type": "warning", 
                             "text": "No puedes eliminar tu propia cuenta" })    
        
        if usuario.groups.all()[0].name == "Administradores":
            return JsonResponse({ "status": False, 
                             "type": "warning", 
                             "text": "No se puede borrar un Administrador" })    
        
        path = "static/uploads/usuarios/" + str(usuario.id) + "/"
        if default_storage.exists(path):
            shutil.rmtree(path)
        
        usuario.delete()
        
        return JsonResponse({ "status": True, 
                             "type": "success", 
                             "text": "El registro ha sido eliminado" })    
