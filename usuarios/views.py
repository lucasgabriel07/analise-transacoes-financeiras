from smtplib import SMTPException
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from . import send_email
import random


def index(request):
    if request.user.is_authenticated:
        return redirect('/importacoes')
    return redirect('login')

def usuarios(request):
    if request.user.is_authenticated:
        usuarios = User.objects.filter(is_superuser=False, is_active=True).order_by('-id')
        context = {
            'usuarios': usuarios,
            'pagina': 'usuarios'
        }
        return render(request, 'usuarios/usuarios.html', context)
    return redirect('login')

def cadastro(request):
    if request.user.is_authenticated:
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
                    'Cadastro realizado com sucesso!'
                )
                return redirect('usuarios')

        context = {'pagina': 'usuarios'}
        return render(request, 'usuarios/cadastro.html', context)

    return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect('/importacoes')
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if empty_field(email) or empty_field(senha):
            messages.error(request, 'Os campos email e senha não podem ficar vazios')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            user = auth.authenticate(request, username=email, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('/importacoes')
            return redirect('login')
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
    
def empty_field(field):
    return field.strip() == ''