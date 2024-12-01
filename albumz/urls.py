from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('<str:album_cod>/', views.album_detail, name='album_detail'),
    path('<str:album_cod>/edit/', views.edit_album, name='edit_album'),
    path('<str:album_cod>/upload/', views.upload_fotos, name='upload_fotos'),  # URL para o upload de fotos
]
