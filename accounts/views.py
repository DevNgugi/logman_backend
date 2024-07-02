from rest_framework import viewsets
from accounts.models import LogmanUser
from accounts.serializers import UserSerializer
from accounts.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    queryset = LogmanUser.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainpairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer