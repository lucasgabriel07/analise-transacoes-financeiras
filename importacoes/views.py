from django.shortcuts import render, redirect
from importacoes.models import Importacao


def index(request):
    if request.user.is_authenticated:
        importacoes = Importacao.objects.order_by('-data_transacoes')
        context = {
            'importacoes': importacoes,
            'pagina': 'importacoes'
        }
        return render(request, 'index.html', context)
    return redirect('login')