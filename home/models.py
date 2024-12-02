from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Adiciona novos campos ao usuário
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # Outros campos adicionais
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_photographer = models.BooleanField(default=False)
    


