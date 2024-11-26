from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Album(models.Model):
    album_nome = models.CharField(max_length=200)
    album_data = models.DateTimeField("date published")
    album_local = models.CharField(max_length=200)


class Fotografo(models.Model):
    fotografo_nome = models.CharField(max_length=200)
    fotografo_email = models.CharField(max_length=200)
    fotografo_data_nasc = models.DateTimeField("date birth")
    fotografo_data_ingr = models.DateTimeField("date joined")

class Foto(models.Model):
    imagem = models.ImageField(upload_to='fotos/')
    foto_desc = models.CharField(max_length=200)
    foto_data = models.DateTimeField("date published")
    foto_fotografo = models.ForeignKey(Fotografo, on_delete=models.CASCADE)
