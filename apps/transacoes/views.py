from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import services
from datetime import datetime
from apps.transacoes.models import Transacao


@login_required
def analise(request):
    data = f'{datetime.now().year}-{datetime.now().month:02}'
    context = {'data': data, 'pagina': 'analise'}
    
    if request.GET.get('mes'):
        data = request.GET.get('mes')
        ano, mes = data.split('-')
        context.update({'data': data})
        
        if Transacao.objects.filter(data_transacao__month=mes, data_transacao__year=ano).exists():
            transacoes_suspeitas = services.transacoes_suspeitas(ano, mes)
            contas_suspeitas = services.contas_suspeitas(ano, mes)
            agencias_suspeitas = services.agencias_suspeitas(ano, mes)
            context.update({
                'transacoes_suspeitas': transacoes_suspeitas,
                'contas_suspeitas': contas_suspeitas,
                'agencias_suspeitas': agencias_suspeitas
            })
        else:
            messages.error(request, 'Não existem transações salvas neste mês.')
    
    return render(request, 'analise.html', context)