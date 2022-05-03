from apps.transacoes.models import Transacao
from apps.importacoes.models import Importacao
from .importador import Importador
from ..exceptions import *
from datetime import datetime
import codecs

class ImportadorCSV(Importador):
    def __init__(self, arquivo):
        super().__init__(arquivo)
        
    def importar_transacoes(self, request):
        if(len(self.arquivo.read()) == 0):
            raise EmptyFileException()
        
        self.qtd_transacoes_validas = 0
        self.qtd_transacoes_invalidas = 0
    
        try:
            dados = list(codecs.iterdecode(self.arquivo, 'utf8'))
            dados_primeira_transacao = dados[0]
            
            data_str = dados_primeira_transacao.split(',')[-1][:10]
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
            
            if self.data_ja_registrada(data):
                raise DateAlreadyRegisteredException

            importacao = Importacao.objects.create(user = request.user,
                                                   data_transacoes = data)
        except ValueError:
            raise InvalidFileException

        for dados_transacao in dados:
            dados_transacao = dados_transacao.replace('\n', '').replace('\r', '')
            
            if self.transacao_valida(dados_transacao, data):
                try:
                    info_transacao = dados_transacao.split(',')
                    banco_origem = info_transacao[0]
                    agencia_origem = info_transacao[1]
                    conta_origem = info_transacao[2]
                    banco_destino = info_transacao[3]
                    agencia_destino = info_transacao[4]
                    conta_destino = info_transacao[5]
                    valor_transacao = float(info_transacao[6])
                    data_transacao = datetime.strptime(info_transacao[7], 
                                                       '%Y-%m-%dT%H:%M:%S')

                    transacao = Transacao.objects.create(
                        importacao = importacao,
                        banco_origem = banco_origem,
                        agencia_origem = agencia_origem,
                        conta_origem = conta_origem,
                        banco_destino = banco_destino,
                        agencia_destino = agencia_destino,
                        conta_destino = conta_destino,
                        valor_transacao = valor_transacao,
                        data_transacao = data_transacao
                    )
                    
                    transacao.save()
                    self.qtd_transacoes_validas += 1
                except ValueError:
                    self.qtd_transacoes_invalidas += 1
            else:
                self.qtd_transacoes_invalidas += 1
        
        if self.qtd_transacoes_validas > 0:
            importacao.save()
        else:
            importacao.delete()

    @staticmethod
    def transacao_valida(dados_transacao, data_arquivo):
        try:
            if len(dados_transacao.strip()) == 0:
                return False
            
            dados = dados_transacao.split(',')
            data_str = dados[-1]
            data = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S')
            
            if (data.year != data_arquivo.year or
                data.month != data_arquivo.month or
                data.day != data_arquivo.day):
                    return False
            
            if len(dados) != 8 or '' in dados:
                return False

            return True

        except ValueError:
            return False