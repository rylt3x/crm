from rest_framework import serializers
from crm import models


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ['client_name', 'client_phone_number', 'client_email', 'client_position', 'client_comment']