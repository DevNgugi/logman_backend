from .models import Connection, Source
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ConnectionSerializer, OrganizationSerializer, SourceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User, Group
from api.models import Organization
from rest_framework import viewsets

# from api.services.crypt import cipher_suite
#     obj = Connection.objects.first()
#     try:
#         plain = (cipher_suite().decrypt(obj.password))
#         print(plain.decode())
#     except Exception as e:

class Sources(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class Connections(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


    def perform_create(self, serializer):
        password = self.request.data.get('ssh_pass')
        if password:
            encrypted_password = serializer.encrypt_password(password)
            serializer.validated_data['ssh_pass'] = encrypted_password
        serializer.save()


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer