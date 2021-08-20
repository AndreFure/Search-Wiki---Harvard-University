from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("wiki/<str:entry>/edit", views.editEntry, name="editEntry"),
    path("wiki/<str:title>/submit", views.submitEditEntry, name="submitEditEntry"),
    path("search", views.search, name="search"),
    path("wiki/", views.randomEntry, name="randomEntry")
]
