from .models import Connection, Source
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ConnectionSerializer, SourceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    
    user = 'user'
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

    # def get_serializer_class(self):

    def perform_create(self, serializer):
        password = self.request.data.get('ssh_pass')
        if password:
            encrypted_password = serializer.convert_password(password)
            serializer.validated_data['ssh_pass'] = encrypted_password
        serializer.save()

    

