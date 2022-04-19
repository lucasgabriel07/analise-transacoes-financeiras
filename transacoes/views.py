from django.shortcuts import render, redirect
from importacoes.models import Importacao
from .submit_form import submit_form


def index(request):
    importacoes = Importacao.objects.order_by('-data_transacoes')
    context = {'importacoes': importacoes}
    return render(request, 'index.html', context)

def upload(request):
    if request.method == 'POST':
        submit_form(request)

    return redirect('index')
