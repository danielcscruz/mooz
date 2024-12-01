from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Album, Foto
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import PermissionDenied

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
    album = get_object_or_404(Album, album_cod=album_cod)
    fotos = album.fotos.all()  # Acessa as fotos relacionadas ao álbum

    # Configurando a paginação
    paginator = Paginator(fotos, 12)  # Exibe 10 fotos por página
    page_number = request.GET.get('page')  # Obtém o número da página da query string
    page_obj = paginator.get_page(page_number)

    return render(request, 'album_detail.html', {
        'album': album,
        'page_obj': page_obj,  # Passa o objeto da página para o template
    })

def edit_album(request, album_cod):
    album = get_object_or_404(Album, album_cod=album_cod)
    
    # Verifica se o usuário tem permissão para editar
    user = request.user
    if not album.edit_permissions.filter(id=user.id).exists():
        return HttpResponseForbidden("Você não tem permissão para editar este álbum.")
    
    if request.method == "POST":
        # Lógica para salvar alterações
        album.title = request.POST.get("title", album.title)
        album.description = request.POST.get("description", album.description)
        album.save()
        return redirect('album_list')  # Redireciona de volta para a lista de álbuns
    
    return render(request, 'edit_album.html', {'album': album})

def upload_fotos(request, album_cod):
    album = get_object_or_404(Album, album_cod=album_cod)
    
    # Verifica se o usuário tem permissão para editar o álbum
    user = request.user
    if not album.edit_permissions.filter(id=user.id).exists():
        raise PermissionDenied("Você não tem permissão para editar este álbum.")
    
    if request.method == 'POST' and request.FILES.getlist('image'):
        # Processa cada arquivo enviado
        for image in request.FILES.getlist('image'):
            Foto.objects.create(imagem=image, album=album)
        
        return JsonResponse({"message": "Upload bem-sucedido!"}, status=200)
    
    return JsonResponse({"error": "Método inválido ou sem arquivos"}, status=400)