from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Album

@receiver(m2m_changed, sender=Album.edit_permissions.through)
def clear_permission_cache(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        # Adicione lógica para invalidar o cache, se necessário
        print(f"Cache invalidado para o álbum: {instance.album_nome}")
