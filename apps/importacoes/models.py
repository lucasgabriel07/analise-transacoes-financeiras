from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Importacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    data_transacoes = models.DateTimeField()
    data_importacao = models.DateTimeField(default=datetime.now)
