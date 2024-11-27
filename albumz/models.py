from django.db import models
from django.contrib.auth.models import User
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
    album_local = models.CharField(max_length=200)
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
    filename = f"{instance.foto_id}.{ext}"  # Não acessa o album_cod ainda
    return os.path.join('fotos', filename)

class Foto(models.Model):
    imagem = models.ImageField(upload_to=foto_upload_path)
    fotografo = models.ForeignKey(Fotografo, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="fotos")
    foto_id = models.PositiveIntegerField(editable=False)  # ID sequencial no álbum
    

    def save(self, *args, **kwargs):
        if not self.pk:  # Apenas ao criar uma nova foto
            last_foto = Foto.objects.filter(album=self.album).order_by('foto_id').last()
            self.foto_id = 1 if not last_foto else last_foto.foto_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Foto {self.foto_id} do álbum {self.album_cod}"
    
class Foto(models.Model):
    imagem = models.ImageField(upload_to=foto_upload_path)
    fotografo = models.ForeignKey(Fotografo, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="fotos")
    foto_id = models.PositiveIntegerField(editable=False)  # ID sequencial no álbum

    def save(self, *args, **kwargs):
        if not self.pk:  # Apenas ao criar uma nova foto
            last_foto = Foto.objects.filter(album=self.album).order_by('foto_id').last()
            self.foto_id = 1 if not last_foto else last_foto.foto_id + 1

        super().save(*args, **kwargs)  # Salva a foto pela primeira vez

        # Após a foto ser salva, ajusta o nome da imagem diretamente
        if self.album and self.foto_id:
            ext = self.imagem.name.split('.')[-1]
            new_name = f"fotos/{self.album.album_cod}_{self.foto_id}.{ext}"
            self.imagem.name = new_name
            # Não chamamos self.save() aqui, apenas atualizamos o campo da imagem
