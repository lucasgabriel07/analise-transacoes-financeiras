from django.shortcuts import render, redirect
from importacoes.models import Importacao
from .submit_form import submit_form


def index(request):
    importacoes = Importacao.objects.order_by('-data_transacoes')
    
    mensagem = request.session.get('message')
    cor = request.session.get('message_color')
        
    context = {
        'importacoes': importacoes,
        'mensagem': mensagem,
        'cor': cor
    }
    
    request.session['message'] = None
    request.session['color'] = None
    
    return render(request,'index.html', context)

def upload(request):
    if request.method == 'POST':
        submit_form(request)
            
    return redirect('index')
