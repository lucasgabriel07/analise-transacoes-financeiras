from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('transacoes.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('admin/', admin.site.urls),
]
