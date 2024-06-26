from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api.views import OrganizationViewSet
from .views import Sources,Connections

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("sources", Sources.as_view()),
    path("connections", Connections.as_view()),
]