from rest_framework import serializers
from .models import SNF

class SNFSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SNF
        fields = ['name', 'description', 'address']
        read_only_fields = ['url', 'created_at', 'updated_at']