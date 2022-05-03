from apps.transacoes.models import Transacao
from apps.importacoes.models import Importacao
from .importador import Importador
from ..exceptions import *
from datetime import datetime
import xml.etree.ElementTree as ET

class ImportadorXML(Importador):
    def __init__(self, arquivo):
        super().__init__(arquivo)
    
    def importar_transacoes(self, request):
        self.qtd_transacoes_validas = 0
        self.qtd_transacoes_invalidas = 0
        
        try:
            tree = ET.parse(self.arquivo)
            root = tree.getroot()
            
            dados = root.findall('./transacao')
            dados_primeira_transacao = dados[0]

            data_str = dados_primeira_transacao.find('./data').text[:10]
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
            
            if self.data_ja_registrada(data):
                raise DateAlreadyRegisteredException

            importacao = Importacao.objects.create(user = request.user,
                                                   data_transacoes = data)
        except (ValueError, TypeError):
            raise InvalidFileException
        
        for dados_transacao in dados:
            if self.transacao_valida(dados_transacao, data):
                try:
                    banco_origem = dados_transacao.find('./origem/banco').text
                    agencia_origem = dados_transacao.find('./origem/agencia').text
                    conta_origem = dados_transacao.find('./origem/conta').text
                    banco_destino = dados_transacao.find('./destino/banco').text
                    agencia_destino = dados_transacao.find('./destino/agencia').text
                    conta_destino = dados_transacao.find('./destino/conta').text
                    valor_transacao = float(dados_transacao.find('./valor').text)
                    data_transacao = datetime.strptime(dados_transacao.find('./data').text, 
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
            data = datetime.strptime(dados_transacao.find('./data').text, 
                              '%Y-%m-%dT%H:%M:%S')
            
            if (data.year != data_arquivo.year or
                data.month != data_arquivo.month or
                data.day != data_arquivo.day):
                    return False
                
            atributos = [
                './origem/banco',
                './origem/agencia',
                './origem/conta',
                './destino/banco',
                './destino/agencia',
                './destino/conta',
                './valor',
                './data'
            ]
            
            for atributo in atributos:
                if (dados_transacao.find(atributo) is None or
                    dados_transacao.find(atributo).text is None):
                    return False
                
            return True
                
        except ValueError:
            return False
