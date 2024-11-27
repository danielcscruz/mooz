from django.shortcuts import render, redirect


def index(request):
    return render(request, 'home.html')

def eventos(request):
    return render(request, 'eventos.html')

def sobre(request):
    return render(request, 'sobre.html')

def fotografos(request):
    return render(request, 'fotografos.html')

def profile(request):
    return render(request, 'profile.html')



