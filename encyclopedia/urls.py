from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<entry>/", views.entry, name="entry"),
    path("wiki/<title>/edit/", views.edit, name="edit"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("wiki/", views.random, name="random")

]
