from django.urls import path

from . import views


urlpatterns = [
    path("log/<str:socket_id>/", views.index, name="index"),
]