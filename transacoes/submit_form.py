from . import csv_handler
from .exceptions import EmptyFileException, InvalidFileException, DateAlreadyRegisteredException


def submit_form(request):
    file = request.FILES['upload']
    message = None
    message_color = None
    green = '#0F520F'
    red = '#AF0C22'
    
    try:
        info = csv_handler.handle(file)
        
        transacoes_validas = info['transacoes_validas']
        transacoes_invalidas = info['transacoes_invalidas']
        
        if transacoes_validas > 0:
            message = (f'Upload completo! {transacoes_validas} transações adicionadas '
                    f'e {transacoes_invalidas} transações inválidas.')
            message_color = green
        
        else:
            message = f'Erro! Nenhuma transação válida. {transacoes_invalidas} transações inválidas'
            message_color = red
    
    except EmptyFileException:
        message = 'Erro! O arquivo está vazio.'
        message_color = red
    
    except InvalidFileException:
        message = 'Erro! Arquivo inválido.'
        message_color = red
    
    except DateAlreadyRegisteredException:
        message = 'Erro! A data das transações já está registrada.'
        message_color = red
    
    finally:
        request.session['message'] = message
        request.session['message_color'] = message_color