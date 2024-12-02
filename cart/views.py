from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from albumz.models import Foto


@login_required
def view_cart(request):
    """Exibe o carrinho do usuário."""
    cart, created = Cart.objects.get_or_create(user=request.user, status='active')
    return render(request, 'cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, photo_id):
    photo = get_object_or_404(Foto, id=photo_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if not cart.items.filter(photo=photo).exists():
        CartItem.objects.create(cart=cart, photo=photo)
    return redirect('album_detail', album_cod=photo.album.album_cod)


@login_required
def remove_from_cart(request, photo_id):
    photo = get_object_or_404(Foto, id=photo_id)
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.items.filter(photo=photo).delete()

    # Pega o parâmetro 'next' da query string
    next_url = request.GET.get('next')
    # Valida se 'next_url' é seguro e redireciona para ele ou para um padrão
    return redirect(resolve_url(next_url) if next_url else 'album_detail', album_cod=photo.album.album_cod)


@login_required
def update_quantity(request, item_id):
    """Atualiza a quantidade de um item no carrinho."""
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove o item se a quantidade for zero
    return redirect('view_cart')
