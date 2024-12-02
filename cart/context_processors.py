from .models import Cart

def cart_item_count(request):
    """Calcula a quantidade total de itens no carrinho do usuário autenticado."""
    total_items = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status='active').first()
        if cart:
            total_items = cart.total_items  # Usa o método total_items do modelo Cart
    return {'cart_item_count': total_items}
