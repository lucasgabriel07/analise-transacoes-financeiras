from smtplib import SMTPException
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .exceptions import *
from . import services

@login_required
def index(request):
    return redirect('/importacoes')

@login_required
def usuarios(request):
    usuarios = User.objects.filter(is_superuser=False, is_active=True).order_by('-id')
    context = {'usuarios': usuarios, 'pagina': 'usuarios'}
    return render(request, 'usuarios/usuarios.html', context)

@login_required
def cadastro(request):
    if request.method == 'POST':        
        try:
            services.cadastrar_usuario(request)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('usuarios')
        except (InvalidFieldException, UserAlreadyExistsException, SendMailException) as e:
            messages.error(request, e.message)
            return redirect('cadastro')
    
    context = {'pagina': 'usuarios'}
    return render(request, 'usuarios/cadastro.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('/importacoes')
    if request.method == 'POST':
        try:
            services.fazer_login(request)
            return redirect('/importacoes')
        except (InvalidFieldException, AuthenticationException) as e:
             messages.error(request, e.message)
             return redirect('login')
         
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def deletar(request, id):
    try:
        services.deletar_usuario(request, id)
        messages.success(request, 'Usuário removido com sucesso!')
    except User.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
    except UserCannotBeDeletedException as e:
        messages.error(request, e.message)
    return redirect('usuarios')

@login_required
def editar(request, id):
    usuario = User.objects.get(id=id)
    
    if request.method == 'POST':
        try:
            services.editar_usuario(request, usuario)
            messages.success(request, 'Alterações salvas!')
        except (InvalidFieldException, UserAlreadyExistsException) as e:
            messages.error(request, e.message)
        return redirect('.')
    
    context = {'usuario': usuario, 'pagina': 'usuarios'}
    return render(request, 'usuarios/editar.html', context)
    

@login_required
def alterar_senha(request, id):
    if request.method == 'POST':
        try:
            services.alterar_senha(request, id)
            messages.success(request, 'Alterações salvas!')
        except AuthenticationException:
            messages.error(request, 'Senha incorreta.')
    return redirect(f'/usuarios/editar/{id}')