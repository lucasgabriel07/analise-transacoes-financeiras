from django.shortcuts import render, redirect
from apps.importacoes.models import Importacao
from apps.transacoes.models import Transacao
from django.contrib.auth.decorators import login_required
from . import services


@login_required
def index(request):
    importacoes = Importacao.objects.order_by('-data_transacoes')
    context = {'importacoes': importacoes, 'pagina': 'importacoes'}
    return render(request, 'index.html', context)

@login_required
def upload(request):
    if request.method == 'POST':
        services.submit_form(request)
    return redirect('index')

@login_required
def detalhar_importacao(request, id):
    importacao = Importacao.objects.get(id=id)
    transacoes = Transacao.objects.filter(importacao=importacao)
    context = {
        'importacao': importacao,
        'transacoes': transacoes,
        'pagina': 'importacoes'
    }
    return render(request, 'transacoes.html', context)