from django.shortcuts import render, redirect
from .submit_form import submit_form


def upload(request):
    if request.user.is_authenticated and request.method == 'POST':
        submit_form(request)
    return redirect('index')
