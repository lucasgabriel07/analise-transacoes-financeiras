from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import services


@login_required
def upload(request):
    if request.method == 'POST':
        services.submit_form(request)
    return redirect('index')