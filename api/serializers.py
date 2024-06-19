from rest_framework import serializers
from .models import Source,Connection
from api.services.crypt import cipher_suite

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'



class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

    def convert_password(self,password):
        try:
            binary_pass = cipher_suite().encrypt(password.encode())
            
            return binary_pass
        
        except Exception as e:
            raise serializers.ValidationError(f"Error encoding password to binary: {str(e)}")

class UserConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id','host']