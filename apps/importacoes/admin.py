from django.contrib import admin
from .models import Importacao

class ImportacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_transacoes', 'data_importacao')
    list_display_links = ('id', 'data_transacoes', 'data_importacao')

admin.site.register(Importacao, ImportacaoAdmin)
