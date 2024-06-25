from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import Sources,Connections

urlpatterns = [
    path("sources", Sources.as_view()),
    path("connections", Connections.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]