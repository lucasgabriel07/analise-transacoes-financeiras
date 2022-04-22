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
            messages.error(request, 'Login e/ou senha inválidos.')
            return redirect('login')
    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def deletar(request, id):
    if request.user.is_authenticated:
        if id != request.user.id:
            try:
                usuario = User.objects.get(id=id)
            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
            else:
                if usuario.is_superuser:
                    messages.error(request, 'Erro! Este usuário não pode ser deletado.')
                else:
                    User.objects.filter(id=id).update(is_active=False)
                    messages.success(request, 'Usuário removido com sucesso!')
        else:
            messages.error(request, 'Erro ao deletar usuário.')
        return redirect('usuarios')
    return redirect('login')

def editar(request, id):
    if request.user.is_authenticated:
        usuario = User.objects.get(id=id)
        
        if request.method == 'POST':
            nome = request.POST['nome']
            email = request.POST['email']
            
            if empty_field(nome):
                messages.error(request, 'O campo nome não pode ficar em branco')
            if empty_field(email):
                messages.error(request, 'O campo email não pode ficar em branco')
                
            if email != usuario.email and User.objects.filter(email=email).exists():
                messages.error(request, 'Já existe um usuário cadastrado com esse email.')
            else:
                User.objects.filter(id=id).update(first_name=nome, email=email, username=email)
                messages.success(request, 'Alterações salvas!')    
            return redirect('.')
        
        context = {
            'usuario': usuario,
            'pagina': 'usuarios'
        }
        return render(request, 'usuarios/editar.html', context)
    
    return redirect('login')

def alterar_senha(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            senha_atual = request.POST['senha']
            nova_senha = request.POST['senha2']
            
            username = User.objects.get(id=id).username

            usuario = auth.authenticate(request, username=username, password=senha_atual)
            if usuario is not None:
                usuario.set_password(nova_senha)
                usuario.save()
                messages.success(request, 'Alterações salvas!')
            else:
                messages.error(request, 'Senha incorreta.')
        return redirect(f'/usuarios/editar/{id}')
    return redirect('login')
    
def empty_field(field):
    return field.strip() == ''