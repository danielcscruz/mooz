from django.db import models
from django.conf import settings
from albumz.models import Foto  # Importa o modelo de fotos do app albumz

class Cart(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('abandoned', 'Abandonado'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrinho {self.id} ({self.user})"

    @property
    def total_value(self):
        """Calcula o valor total do carrinho somando os valores dos itens."""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Calcula o número total de itens no carrinho, somando as quantidades de cada item."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    photo = models.ForeignKey(
        Foto,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.photo} (Carrinho {self.cart.id})"

    @property
    def total_price(self):
        """Calcula o preço total do item no carrinho."""
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        # Atualiza o preço com o valor do álbum associado
        if not self.pk:  # Apenas ao criar um novo item no carrinho
            self.price = self.photo.album.album_valor
            # Verifica se o item já existe no carrinho, se sim, incrementa a quantidade
            existing_item = CartItem.objects.filter(cart=self.cart, photo=self.photo).first()
            if existing_item:
                # Se o item já estiver no carrinho, aumenta a quantidade
                existing_item.quantity += self.quantity
                existing_item.save()
                return  # Não cria um novo item
        super().save(*args, **kwargs)
