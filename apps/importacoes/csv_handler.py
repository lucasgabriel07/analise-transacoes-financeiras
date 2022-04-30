import codecs
from datetime import datetime
from apps.transacoes.models import Transacao
from apps.importacoes.models import Importacao
from .exceptions import *


def handle(request, file):
    if(len(file.read()) == 0):
        raise EmptyFileException()
    
    data = codecs.iterdecode(file, 'utf8')
    
    transacoes_validas = 0
    transacoes_invalidas = 0

    for index, line in enumerate(data):
        line = line.replace('\n', '').replace('\r', '')
        
        if index == 0:
            try:
                date_str = line.split(',')[-1][:10]
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                
                if (date_is_already_registered(date)):
                    raise DateAlreadyRegisteredException
            except ValueError:
                raise InvalidFileException
            else:
                importacao = Importacao.objects.create(
                    user = request.user,
                    data_transacoes = date
                )
        
        if line_is_valid(line, date):
            try:
                info_transacao = line.split(',')
                banco_origem = info_transacao[0]
                agencia_origem = info_transacao[1]
                conta_origem = info_transacao[2]
                banco_destino = info_transacao[3]
                agencia_destino = info_transacao[4]
                conta_destino = info_transacao[5]
                valor_transacao = float(info_transacao[6])
                data_transacao = datetime.strptime(info_transacao[7], '%Y-%m-%dT%H:%M:%S')

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
                transacoes_validas += 1
            except ValueError:
                transacoes_invalidas += 1
        else:
            transacoes_invalidas += 1
    
    if transacoes_validas > 0:
        importacao.save()
    else:
        importacao.delete()
    
    return transacoes_validas, transacoes_invalidas

def line_is_valid(line, file_date):
    try:
        if len(line.strip()) == 0:
            return False
        
        values = line.split(',')
        if len(values) != 8 or '' in values:
            return False
        
        date_str = values[-1]
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        
        if (date.year != file_date.year or
            date.month != file_date.month or
            date.day != file_date.day):
                return False

        return True

    except ValueError:
        return False

def date_is_already_registered(date):
    return Importacao.objects.filter(data_transacoes=date).exists()
