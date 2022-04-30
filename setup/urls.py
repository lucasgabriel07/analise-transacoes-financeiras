from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.usuarios.urls')),
    path('importacoes/', include('apps.importacoes.urls')),
    path('transacoes/', include('apps.transacoes.urls')),
    path('admin/', admin.site.urls),
]
