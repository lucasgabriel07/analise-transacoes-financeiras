from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from setup.settings import EMAIL_HOST_USER
from .exceptions import *
import random

    
def cadastrar_usuario(request):
    nome = request.POST['nome']
    email = request.POST['email']
    
    if campo_em_branco(nome):
        raise InvalidFieldException('O campo nome não pode ficar em branco')
    
    if campo_em_branco(email):
        raise InvalidFieldException('O campo email não pode ficar em branco')
    
    if User.objects.filter(email=email).exists():
        raise UserAlreadyExistsException
    
    password = str(random.randint(100000, 999999))
        
    try:
        send_mail(
            'Cadastro realizado com sucesso!',
            f'Seu cadastro foi realizado com sucesso! Sua senha é {password}.',
            EMAIL_HOST_USER,
            email,
            fail_silently=False
        )
    except:
        raise SendMailException
    else:
        user = User.objects.create_user(
            first_name=nome, 
            username=email,
            email=email, 
            password=password
        )
        user.save()
        
def fazer_login(request):
    email = request.POST['email']
    senha = request.POST['senha']
   
    if campo_em_branco(email):
        raise InvalidFieldException('O campo email não pode ficar em branco')

    if not User.objects.filter(email=email).exists():
        raise AuthenticationException
    
    user = auth.authenticate(request, username=email, password=senha)
    if user is None:
        raise AuthenticationException
    
    auth.login(request, user)
    
def deletar_usuario(request, id):
    if id == request.user.id or User.objects.get(id=id).is_superuser:
        raise UserCannotBeDeletedException
    User.objects.filter(id=id).update(is_active=False)
    
def editar_usuario(request, usuario):
    nome = request.POST['nome']
    email = request.POST['email']
    
    if campo_em_branco(nome):
        raise InvalidFieldException('O campo nome não pode ficar em branco')
    
    if campo_em_branco(email):
        raise InvalidFieldException('O campo email não pode ficar em branco')
        
    if email != usuario.email and User.objects.filter(email=email).exists():
        raise UserAlreadyExistsException
    
    User.objects.filter(id=usuario.id).update(first_name=nome, email=email, username=email)
    
def alterar_senha(request, id):
    senha_atual = request.POST['senha']
    nova_senha = request.POST['senha2']
    
    username = User.objects.get(id=id).username
    user = auth.authenticate(request, username=username, password=senha_atual)
    
    if user is None:
        raise AuthenticationException
    
    user.set_password(nova_senha)
    user.save()
    
def campo_em_branco(campo):
    return campo.strip() == ''