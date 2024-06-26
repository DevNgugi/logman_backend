from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.models import LogmanUser
from accounts.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = LogmanUser.objects.all()
    serializer_class = UserSerializer

