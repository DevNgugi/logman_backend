from rest_framework import serializers
from .models import Organization, Source,Connection
from api.utils.crypt import cipher_suite
from api.utils.generators import generate_code



class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['ssh_user','ssh_host','ssh_port','id']
 
class SourceSerializer(serializers.ModelSerializer):

    connection = serializers.PrimaryKeyRelatedField(
        queryset=Connection.objects.all(), write_only=True
    )
    connection_details = ConnectionSerializer(source='connection', read_only=True)


    class Meta:
        model = Source
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(SourceSerializer, self).to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%d-%m-%y %H:%M:%S')
        representation['modified_at'] = instance.created_at.strftime('%d-%m-%y %H:%M:%S')
        representation['connection'] = ConnectionSerializer(instance.connection).data

        return representation
       
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