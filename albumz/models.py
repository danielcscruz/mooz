from django.db import models
from django.contrib.auth.models import User
from home.models import CustomUser
import os
import random, string
# Create your models here.

def generate_album_cod():
    """Gera um ID aleatório de 6 caracteres, com letras maiúsculas e números."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Album(models.Model):
    album_cod = models.CharField(max_length=6, unique=True, editable=False, default=generate_album_cod)
    album_nome = models.CharField(max_length=200)
    album_data = models.DateField("date published")
    album_desc = models.CharField(max_length=200, blank=True )
    album_local = models.CharField(max_length=200)
    album_cover = models.ImageField(upload_to='album_covers/', null=True, blank=True)
    edit_permissions = models.ManyToManyField(
        CustomUser,
        related_name="editable_albums",
        blank=True  # Permite que o campo seja opcional
    )
    def __str__(self):
        return self.album_nome

class Fotografo(models.Model):
    fotografo_nome = models.CharField(max_length=200)
    fotografo_email = models.CharField(max_length=200)
    fotografo_data_nasc = models.DateField("date birth")
    fotografo_data_ingr = models.DateField("date joined")
    def __str__(self):
        return self.fotografo_nome

def foto_upload_path(instance, filename):
    # Gera o nome do arquivo sem tentar acessar o album_cod diretamente
    ext = filename.split('.')[-1]
    filename = f"{instance.al_cod}_{instance.foto_id}.{ext}"  # Não acessa o album_cod ainda
    return os.path.join('fotos', filename)

    
class Foto(models.Model):
    imagem = models.ImageField(upload_to=foto_upload_path)
    fotografo = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="fotos")
    foto_id = models.PositiveIntegerField(editable=False)
   
    def save(self, *args, **kwargs):
        if not self.pk:  # Apenas ao criar uma nova foto
            last_foto = Foto.objects.filter(album=self.album).order_by('foto_id').last()
            self.foto_id = 1 if not last_foto else last_foto.foto_id + 1
        super().save(*args, **kwargs)
 # Propriedade que herda o valor de album_cod
    @property
    def al_cod(self):
        return self.album.album_cod if self.album else None

    # Propriedade que herda o valor de album_nome
    @property
    def al_desc(self):
        return self.album.album_nome if self.album else None

    def __str__(self):
        return os.path.basename(self.imagem.name) if self.imagem else "Sem imagem"    
