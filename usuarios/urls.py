from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/deletar/<int:id>/', views.deletar, name="deletar_usuario"),
    path('usuarios/editar/<int:id>/', views.editar, name="editar_usuario"),
    path('usuarios/alterar_senha/<int:id>/', views.alterar_senha, name="alterar_senha"),
]
