from django.contrib import admin
from .models import Transacao

class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_transacao', 'valor_transacao', 'data_upload')
    list_display_links = ('id', 'data_transacao', 'valor_transacao', 'data_upload')

admin.site.register(Transacao, TransacaoAdmin)
