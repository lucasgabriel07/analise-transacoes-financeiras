from django.db import models
from datetime import datetime
from apps.importacoes.models import Importacao


class Transacao(models.Model):
    importacao = models.ForeignKey(Importacao, on_delete=models.RESTRICT)
    banco_origem = models.CharField(max_length=100)
    agencia_origem = models.CharField(max_length=4)
    conta_origem = models.CharField(max_length=7)
    banco_destino = models.CharField(max_length=100)
    agencia_destino = models.CharField(max_length=4)
    conta_destino = models.CharField(max_length=7)
    valor_transacao = models.FloatField()
    data_transacao = models.DateTimeField()
    data_upload = models.DateTimeField(default=datetime.now)
    
    class Meta:
        verbose_name_plural = "transações"
