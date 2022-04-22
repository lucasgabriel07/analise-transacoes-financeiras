from django.shortcuts import render, redirect
from importacoes.models import Importacao
from transacoes.models import Transacao
from django.template.defaulttags import register


def index(request):
    if request.user.is_authenticated:
        importacoes = Importacao.objects.order_by('-data_transacoes')
        context = {
            'importacoes': importacoes,
            'pagina': 'importacoes'
        }
        return render(request, 'index.html', context)
    return redirect('login')

def detalhar_importacao(request, id):
    if request.user.is_authenticated:
        importacao = Importacao.objects.get(id=id)
        transacoes = Transacao.objects.filter(importacao=importacao)
        context = {
            'importacao': importacao,
            'transacoes': transacoes,
            'pagina': 'importacoes',
        }
        return render(request, 'transacoes.html', context)
    return redirect('login')

@register.filter
def mask_money(valor_transacao):
    return f'R$ {valor_transacao:.2f}'.replace('.', ',')