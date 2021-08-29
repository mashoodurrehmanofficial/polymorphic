from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import threading
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from authx.models import ValidateCode

def loginx(request):
    
    if request.user.is_authenticated:
        return redirect("/vacas")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            user_v = User.objects.get(username=username).is_active
            if user_v != True:
                return redirect('/auth/verification')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("/vacas")
        else:
            messages.error(request, "Inicio de sesión no válido")
            return redirect("/auth/login")
    return render(request, "auth/login.html")

def logoutx(request):
    logout(request)
    return redirect("/auth/login")

def forgot(request):
    
    if request.user.is_authenticated:
        return redirect("/vacas")
    
    if request.method == "POST":
        email = request.POST["email"]
        
        user = User.objects.filter(email = email).first()
        
        if user is not None:
            usuario_pass = get_random_string(length=8)
            usuario_pass_hashed = make_password(usuario_pass)
            user.password = usuario_pass_hashed
            user.save()
            send_mail(
                'Recuperación de contraseña',
                'Hola! Tu nueva contraseña es: ' + usuario_pass + '. Ya puedes acceder a tu cuenta.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )            
            messages.success(request, "Te hemos enviado un correo con tu nueva contraseña")
            return redirect("/auth/login")
        else:
            messages.error(request, "Correo electrónico no registrado")
            return redirect("/auth/forgot")
    
    return render(request, "auth/forgot.html")

def activateAccount(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None  and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, "Su cuenta ha sido Validada!")
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')

def verification(request):
    if request.method == "POST":
        code = request.POST.get("code")
        if ValidateCode.objects.filter(code=code).exists():
            code_user = ValidateCode.objects.get(code__iexact=code).user_id
            user_v = User.objects.get(id=code_user)
            user_v.is_active = True
            user_v.save()
            messages.success(request, "Su cuenta ha sido Validada!")
            return redirect('/auth/login')
        else:
            messages.error(request, "No hay codigo.")
            return redirect('/auth/login')
    return render(request, "auth/verification.html")

