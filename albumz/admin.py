from django.contrib import admin

# Register your models here.

from .models import Foto, Fotografo, Album



admin.site.register(Foto)
admin.site.register(Album)
admin.site.register(Fotografo)