from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:photo_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:photo_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'),
]