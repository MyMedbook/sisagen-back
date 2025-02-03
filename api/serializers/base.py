# api/serializers/base.py
from rest_framework import serializers
import requests
from api.models.base import Status

class StructureSerializer(serializers.Serializer):
    """Base serializer for Sisagen Structures"""
    id = serializers.IntegerField(required=True)
    name = serializers.CharField()

    def to_internal_value(self, data):

        id = data['id']
        structure_url = f"https://mymedbook.it/api/v1/structure/{id}/?label=sisagen"
        auth_header = self.context["request"].META.get('HTTP_AUTHORIZATION')
        headers = {"Authorization": auth_header}

        struct_response = requests.get(
                structure_url,
                headers=headers
            )
        
        if struct_response.status_code == 404:
            raise serializers.ValidationError(f"No Sisagen structure found with id {id}")
        
        data["name"] = struct_response.json()["name"]

        return super().to_internal_value(data)

class BaseSerializer(serializers.Serializer):
    """Base serializer with common fields"""
    paziente_id = serializers.IntegerField(required=True)
    operatore_id = serializers.IntegerField(required=True)
    datamanager_id = serializers.IntegerField(required=True)
    structure = StructureSerializer(required=True)
    status = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in Status], 
        default=Status.DRAFT
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_paziente_id(self, value):
        """Validate paziente_id is positive"""
        if value <= 0:
            raise serializers.ValidationError("paziente_id must be positive")
        return value

    def validate_operatore_id(self, value):
        """Validate operatore_id is positive"""
        if value <= 0:
            raise serializers.ValidationError("operatore_id must be positive")
        return value

    def to_internal_value(self, data):

        data["datamanager_id"] = self.context["request"].user.pk

        return super().to_internal_value(data)