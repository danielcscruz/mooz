from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('new/', views.new_album, name='new_album'),
    path('<str:album_cod>/', views.album_detail, name='album_detail'),
    path('<str:album_cod>/edit/', views.edit_album, name='edit_album'),
    path('<str:album_cod>/edit_info/', views.edit_info_album, name='edit_info_album'),
    path('<str:album_cod>/upload/', views.upload_fotos, name='upload_fotos'),  # URL para o upload de fotos
    path('<str:album_cod>/photos/', views.get_album_photos, name='get_album_photos'),
    path('<str:album_cod>/<int:foto_id>/delete/', views.delete_photo, name='delete_photo'),
    path('album/<str:album_cod>/delete/', views.delete_album, name='delete_album'),


]
