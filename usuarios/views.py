from smtplib import SMTPException
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from . import send_email
import random


def usuarios(request):
    usuarios = User.objects.order_by('-id')
    context = { 'usuarios': usuarios}
    return render(request, 'usuarios/usuarios.html', context)

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        
        if empty_field(nome):
            messages.error(request, 'O campo nome não pode ficar em branco')
            return redirect('cadastro')
        if empty_field(email):
            messages.error(request, 'O campo email não pode ficar em branco')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        
        password = str(random.randint(100000, 999999))
        
        try:
            send_email.send(
                email,
                'Cadastro realizado com sucesso!',
                f'Seu cadastro foi realizado com sucesso! Sua senha é {password}.'
            )
        except:
            messages.error(request, 'Erro ao enviar email.')
            return redirect('cadastro')
        else:
            user = User.objects.create_user(
                first_name=nome, 
                username=email,
                email=email, 
                password=password
            )
            user.save()
            messages.success(
                request, 
                'Cadastro realizado com sucesso! Sua senha foi enviada para o seu email'
            )
            return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    return render(request, 'usuarios/login.html')

def logout(request):
    pass

def dashboard(request):
    pass

def empty_field(field):
    return field.strip() == ''