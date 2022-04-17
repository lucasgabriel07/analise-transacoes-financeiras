from django.db import models
from datetime import datetime


class Transacao(models.Model):
    banco_origem = models.CharField(max_length=100)
    agencia_origem = models.CharField(max_length=4)
    conta_origem = models.CharField(max_length=7)
    banco_destino = models.CharField(max_length=100)
    agencia_destino = models.CharField(max_length=4)
    conta_destino = models.CharField(max_length=7)
    valor_transacao = models.FloatField()
    data_transacao = models.DateTimeField()
    data_upload = models.DateTimeField(default=datetime.now)
