from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm



def index(request):
    return render(request, 'home.html')

def eventos(request):
    return render(request, 'eventos.html')

def sobre(request):
    return render(request, 'sobre.html')

def fotografos(request):
    return render(request, 'fotografos.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para a página de login após o registro
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

