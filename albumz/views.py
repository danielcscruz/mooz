from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Album



# def album_list(request):
#    albums = Album.objects.prefetch_related('fotos').all()  # Carrega álbuns e fotos associadas
#    return render(request, 'album_list.html', {'albums': albums})

def album_list(request):
    albums = Album.objects.all()  # Consulta para buscar os álbuns
    paginator = Paginator(albums, 8)  # Mostre 8 álbuns por página (ajuste conforme necessário)
    
    # Obtenha o número da página da query string (?page=)
    page_number = request.GET.get('page')
    page_albums = paginator.get_page(page_number)  # Retorna os álbuns da página atual

    return render(request, 'album_list.html', {'albums': page_albums})

def album_detail(request, album_cod):
    # Busca o álbum pelo ID
    album = get_object_or_404(Album, id=album_cod)
    
    # Aqui você pode acessar as fotos do álbum, supondo que você tenha uma relação de fotos (ex: uma ForeignKey ou ManyToMany)
    # Exemplo: fotos = album.fotos.all()
    # Supondo que o modelo de Foto tenha uma relação com o Album e tenha um campo 'image' para armazenar a imagem
    fotos = album.fotos.all()  # Caso tenha um modelo Foto com ForeignKey para Album
    
    return render(request, 'album_detail.html', {'album': album, 'fotos': fotos})