from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('<int:id>/', views.detalhar_importacao, name='detalhar_importacao'),
]