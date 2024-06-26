from rest_framework import serializers
from .models import Organization, Source,Connection
from api.utils.crypt import cipher_suite
from api.utils.generators import generate_code

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'



class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

    def encrypt_password(self,password):
        try:
            binary_pass = cipher_suite().encrypt(password.encode())
            
            return binary_pass
        
        except Exception as e:
            raise serializers.ValidationError(f"Error encoding password to binary: {str(e)}")

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['title','code']
        extra_kwargs = {
            'code': {'read_only': True},
        }
    
    def create(self, validated_data):
        validated_data['code'] = generate_code(8)
        return Organization.objects.create(**validated_data)