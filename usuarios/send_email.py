from django.core.mail import send_mail
from analise_transacoes.settings import EMAIL_HOST_USER


def send(user_email, subject, message):
    send_mail(
    subject,
    message,
    EMAIL_HOST_USER,
    [user_email],
    fail_silently=False,
)