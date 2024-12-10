from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Album, Foto
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.models import CartItem

# def album_list(request):
#    albums = Album.objects.prefetch_related('fotos').all()  # Carrega álbuns e fotos associadas
#    return render(request, 'album_list.html', {'albums': albums})

def album_list(request):
    albums = Album.objects.all().order_by('-album_data') # Consulta para buscar os álbuns
    paginator = Paginator(albums, 8)  # Mostre 8 álbuns por página (ajuste conforme necessário)
    
    # Obtenha o número da página da query string (?page=)
    page_number = request.GET.get('page')
    page_albums = paginator.get_page(page_number)  # Retorna os álbuns da página atual

    return render(request, 'album_list.html', {'albums': page_albums})

def album_detail(request, album_cod):
    # Obter o álbum e suas fotos
    album = get_object_or_404(Album, album_cod=album_cod)
    fotos = album.fotos.all()

    # Inicializar variáveis para usuários não autenticados
    cart_item_ids = []

    # Se o usuário estiver autenticado, acessar o carrinho
    if request.user.is_authenticated:
        cart = request.user.carts.filter(status='active').first()
        if cart:
            cart_item_ids = list(cart.items.values_list('photo_id', flat=True))  # IDs das fotos no carrinho

    context = {
        'album': album,
        'page_obj': fotos,  # Fotos paginadas ou não
        'cart_item_ids': cart_item_ids,
    }
    return render(request, 'album_detail.html', context)


def edit_album(request, album_cod):
    album = get_object_or_404(Album, album_cod=album_cod)
    
    # Verifica se o usuário tem permissão para editar
    user = request.user
    if not album.edit_permissions.filter(id=user.id).exists():
        return HttpResponseForbidden("Você não tem permissão para editar este álbum.")
    
    if request.method == "POST":
        # Lógica para salvar alterações
        album.title = request.POST.get("title", album.album_nome)
        album.description = request.POST.get("description", album.album_local)
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
            Foto.objects.create(imagem=image, album=album,fotografo=request.user)
        
        return JsonResponse({"message": "Upload bem-sucedido!"}, status=200)
    
    return JsonResponse({"error": "Método inválido ou sem arquivos"}, status=400)


def get_album_photos(request, album_cod):
    album = get_object_or_404(Album, album_cod=album_cod)
    fotos = album.fotos.all()
    data = [
        {
            "foto_id": foto.foto_id,
            "name": foto.imagem.name,
            "url": foto.imagem.url,
        }
        for foto in fotos
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt  # Necessário para métodos DELETE
def delete_photo(request, album_cod, foto_id):
    if request.method == "DELETE":
        try:
            # Verifica se o álbum existe
            album = get_object_or_404(Album, album_cod=album_cod)
            foto = Foto.objects.get(foto_id=foto_id, album=album)
            foto.delete()
            return JsonResponse({"message": "Foto deletada com sucesso!"}, status=200)
        except Foto.DoesNotExist:
            return JsonResponse({"error": "Foto nao encontrada."}, status=404)
    return JsonResponse({"error": "metodo invalido."}, status=405)

def edit_info_album(request, album_cod):
    album = get_object_or_404(Album, album_cod=album_cod)
    
    # Verifica se o usuário tem permissão para editar
    user = request.user
    if not album.edit_permissions.filter(id=user.id).exists():
        return HttpResponseForbidden("Você não tem permissão para editar este álbum.")
    
    if request.method == "POST":
        # Lógica para salvar alterações
        album.album_nome = request.POST.get("title", album.album_nome)
        album.album_data = request.POST.get("date", album.album_data)
        album.album_local = request.POST.get("local", album.album_local)
        album.album_desc = request.POST.get("desc", album.album_desc)
        album.album_cover = request.POST.get("cover", album.album_cover)
         # Verifica se o campo 'cover' foi enviado
        if request.FILES.get("cover"):
            album.album_cover = request.FILES["cover"]  # Capa do álbum
        
        album.save()
        return redirect('edit_album', album_cod=album.album_cod)  # Redireciona de volta para a lista de álbuns
    
    return render(request, 'edit_info_album.html', {'album': album})


def new_album(request):
    user = request.user

    # Verifica se o usuário está autenticado e é um fotógrafo
    if not user.is_authenticated or not user.is_photographer:
        return HttpResponseForbidden("Você não tem permissão para criar um álbum.")

    if request.method == "POST":
        # Criação de um novo álbum
        album_nome = request.POST.get("title", "")
        album_data = request.POST.get("date", None)
        album_local = request.POST.get("local", "")
        album_desc = request.POST.get("desc", "")
        album_cover = request.FILES.get("cover", None)

        # Valida se os campos obrigatórios foram preenchidos
        if not album_nome or not album_data:
            return render(request, 'new_album.html', {
                'error_message': "Título e Data são obrigatórios."
            })

        # Cria o objeto Album
        album = Album(
            album_nome=album_nome,
            album_data=album_data,
            album_local=album_local,
            album_desc=album_desc,
            album_cover=album_cover
        )
        album.save()

        # Adiciona o criador ao grupo edit_permissions
        album.edit_permissions.add(user)
        album.save()  # Salva novamente para garantir a persistência

        return redirect('album_list')  # Redireciona para a lista de álbuns

    return render(request, 'new_album.html')

def delete_album(request, album_cod):
    if request.method == "POST":
        album = get_object_or_404(Album, album_cod=album_cod)
        # Verifica se o usuário tem permissão para excluir
        if request.user not in album.edit_permissions.all():
            return HttpResponseForbidden("Você não tem permissão para excluir este álbum.")
        
        album.delete()
        return redirect('album_list')  # Redireciona para a lista de álbuns

        