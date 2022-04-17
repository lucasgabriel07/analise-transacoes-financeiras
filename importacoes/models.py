from django.db import models
from datetime import datetime


class Importacao(models.Model):
    data_transacoes = models.DateTimeField()
    data_importacao = models.DateTimeField(default=datetime.now)
