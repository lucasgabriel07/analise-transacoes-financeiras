from django.db.models import Sum, F
from .models import Transacao


def transacoes_suspeitas(ano, mes):
    transacoes_suspeitas = Transacao.objects.filter(data_transacao__month=mes, 
                                                    data_transacao__year=ano,
                                                    valor_transacao__gte=100_000)
    return transacoes_suspeitas

def contas_suspeitas(ano, mes):
    transacoes = Transacao.objects.filter(data_transacao__month=mes,
                                          data_transacao__year=ano)
    
    contas_origem = (transacoes.values('banco_origem', 'agencia_origem', 'conta_origem')
                               .annotate(valor_movimentado=Sum('valor_transacao'),
                                        banco=F('banco_origem'),
                                        agencia=F('agencia_origem'),
                                        conta=F('conta_origem'))
                               .filter(valor_movimentado__gt=1_000_000))
    
    contas_destino = (transacoes.values('banco_destino', 'agencia_destino', 'conta_destino')
                                .annotate(valor_movimentado=Sum('valor_transacao'),
                                        banco=F('banco_destino'),
                                        agencia=F('agencia_destino'),
                                        conta=F('conta_destino'))
                                .filter(valor_movimentado__gt=1_000_000))
    
    for conta in contas_origem:
        conta.update({'tipo_movimentacao': 'Saída'})
    
    for conta in contas_destino:
        conta.update({'tipo_movimentacao': 'Entrada'})
        
    contas_suspeitas = list(contas_origem) + list(contas_destino)

    return contas_suspeitas

def agencias_suspeitas(ano, mes):
    transacoes = Transacao.objects.filter(data_transacao__month=mes,
                                          data_transacao__year=ano)
    
    agencias_origem = (transacoes.values('banco_origem', 'agencia_origem')
                               .annotate(valor_movimentado=Sum('valor_transacao'),
                                        banco=F('banco_origem'),
                                        agencia=F('agencia_origem'))
                               .filter(valor_movimentado__gt=1_000_000_000))
    
    agencias_destino = (transacoes.values('banco_destino', 'agencia_destino')
                               .annotate(valor_movimentado=Sum('valor_transacao'),
                                        banco=F('banco_destino'),
                                        agencia=F('agencia_destino'))
                               .filter(valor_movimentado__gt=1_000_000_000))
    
    for agencia in agencias_origem:
        agencia.update({'tipo_movimentacao': 'Saída'})
    
    for agencia in agencias_destino:
        agencia.update({'tipo_movimentacao': 'Entrada'})
        
    agencias_suspeitas = list(agencias_origem) + list(agencias_destino)
    
    return agencias_suspeitas