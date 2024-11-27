from django.shortcuts import render
from .models import Album

def album_list(request):
    albums = Album.objects.prefetch_related('fotos').all()  # Carrega álbuns e fotos associadas
    return render(request, 'album_list.html', {'albums': albums})