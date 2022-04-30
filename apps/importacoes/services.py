from django.template.defaulttags import register

@register.filter
def mask_money(valor_transacao):
    return f'R$ {valor_transacao:.2f}'.replace('.', ',')