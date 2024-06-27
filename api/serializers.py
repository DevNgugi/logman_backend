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
        fields = ['ssh_user','ssh_host','ssh_port']
        
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