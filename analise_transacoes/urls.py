from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('usuarios.urls')),
    path('importacoes/', include('importacoes.urls')),
    path('transacoes/', include('transacoes.urls')),
    path('admin/', admin.site.urls),
]
