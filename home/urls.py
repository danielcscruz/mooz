from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("eventos/", views.eventos, name="eventos"),
    path("fotografos/", views.fotografos, name = "fotografos"),
    path("sobre/", views.sobre, name = "sobre"),

]