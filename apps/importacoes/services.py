from django.template.defaulttags import register
from django.contrib import messages
from . import csv_handler
from .exceptions import *


def submit_form(request):
    file = request.FILES['upload']
    
    try:
        transacoes_validas, transacoes_invalidas = csv_handler.handle(request, file)

        if transacoes_validas > 0:
            message = (f'Upload completo! {transacoes_validas} transações adicionadas '
                    f'e {transacoes_invalidas} transações inválidas.')
            messages.success(request, message)

        else:
            message = f'Erro! Nenhuma transação válida. {transacoes_invalidas} transações inválidas.'
            messages.error(request, message)
    
    except EmptyFileException:
        message = 'Erro! O arquivo está vazio.'
        messages.error(request, message)
        
    except InvalidFileException:
        message = 'Erro! Arquivo inválido.'
        messages.error(request, message)
    
    except DateAlreadyRegisteredException:
        message = 'Erro! A data das transações já está registrada.'
        messages.error(request, message)

@register.filter
def mask_money(valor_transacao):
    return f'R$ {valor_transacao:.2f}'.replace('.', ',')