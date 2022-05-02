from django.urls import path

from . import views

urlpatterns = [
    path('analise/', views.analise, name='analise'),
]
