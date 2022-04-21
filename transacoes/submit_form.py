from django.contrib import messages
from . import csv_handler
from .exceptions import EmptyFileException, InvalidFileException, DateAlreadyRegisteredException
from importacoes.models import Importacao


def submit_form(request):
    file = request.FILES['upload']
    
    try:
        data_transacoes, transacoes_validas, transacoes_invalidas = csv_handler.handle(file)

        if transacoes_validas > 0:
            importacao = Importacao.objects.create(
                user = request.user,
                data_transacoes = data_transacoes
            )
            importacao.save()
            message = (f'Upload completo! {transacoes_validas} transações adicionadas '
                    f'e {transacoes_invalidas} transações inválidas.')
            messages.success(request, message)

        else:
            message = f'Erro! Nenhuma transação válida. {transacoes_invalidas} transações inválidas'
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
