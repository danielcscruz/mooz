from django.apps import AppConfig


class AlbumzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'albumz'

    def ready(self):
        import albumz.signals  # Certifique-se de usar o nome correto do app