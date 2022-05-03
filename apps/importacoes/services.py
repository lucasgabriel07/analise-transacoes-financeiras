from django.template.defaulttags import register
from django.contrib import messages
from .importador.importador_csv import ImportadorCSV
from .importador.importador_xml import ImportadorXML
from .exceptions import *
import locale


def submit_form(request):
    file = request.FILES['upload']
    
    try:
        if file.name.endswith('.csv'):
            importador = ImportadorCSV(file)
        elif file.name.endswith('.xml'):
            importador = ImportadorXML(file)
        else:
            message = 'Erro! Arquivo inválido'
            messages.error(request, message)
            return

        importador.importar_transacoes(request)
        qtd_transacoes_validas = importador.qtd_transacoes_validas
        qtd_transacoes_invalidas = importador.qtd_transacoes_invalidas
        
        if qtd_transacoes_validas > 0:
            message = (f'Upload completo! {qtd_transacoes_validas} transações adicionadas '
                        f'e {qtd_transacoes_invalidas} transações inválidas.')
            messages.success(request, message)

        else:
            message = (f'Erro! Nenhuma transação válida. '
                        f'{qtd_transacoes_invalidas} transações inválidas.')
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
def format_money(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(valor, grouping=True)