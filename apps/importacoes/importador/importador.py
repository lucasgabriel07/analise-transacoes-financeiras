from abc import ABC, abstractmethod
from apps.importacoes.models import Importacao

class Importador(ABC):
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.qtd_transacoes_validas = None
        self.qtd_transacoes_invalidas = None
    
    @abstractmethod
    def importar_transacoes(self, request):
        pass
    
    @staticmethod
    @abstractmethod
    def transacao_valida(dados_transacao, data_arquivo):
        pass
    
    @staticmethod
    def data_ja_registrada(data_transacoes):
        return Importacao.objects.filter(data_transacoes=data_transacoes).exists()