from django.http import JsonResponse
from .models import Connection, Source
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ConnectionSerializer, OrganizationSerializer, SourceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User, Group
from api.models import Organization
from rest_framework import viewsets
from api.utils.crypt import cipher_suite
from rest_framework.response import Response

from rest_framework import status


# from api.services.crypt import cipher_suite
#     obj = Connection.objects.first()
#     try:
#         plain = (cipher_suite().decrypt(obj.password))
#         print(plain.decode())
#     except Exception as e:

class Sources(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        file_path = validated_data['file_path']
        connection = validated_data['connection']
        existing_sources = Source.objects.filter(file_path=file_path, connection=connection)
        if existing_sources.exists():
            return Response({'error': 'Source with similar details exists'}, status=404)
        
        source = Source.objects.create(**validated_data)
        return Response(SourceSerializer(source).data, status=201)
            

class Connections(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

    def create(self, request, *args, **kwargs):
        ssh_pass = self.request.data.get('ssh_pass')
        ssh_user = self.request.data.get('ssh_user')
        ssh_host = self.request.data.get('ssh_host')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if ssh_pass:
            encrypted_password = cipher_suite().encrypt(ssh_pass.encode())
            serializer.validated_data['ssh_pass'] = encrypted_password
        else:
            return Response({'error': 'ssh password is required'}, status=404)

        # no host should have the same password & username
        existing_connections = Connection.objects.filter(ssh_host=ssh_host, ssh_user = ssh_user)

        if existing_connections.exists():
            return Response({'error': 'Connection exists!'}, status=404)
        serializer.save()
        return Response(request.data, status=200)

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer