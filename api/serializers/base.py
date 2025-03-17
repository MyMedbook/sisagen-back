# api/serializers/base.py
from rest_framework import serializers
import requests
from api.models.base import Status

class StructureSerializer(serializers.Serializer):
    """Base serializer for Sisagen Structures"""
    pk = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    max_members = serializers.CharField(allow_blank=True, allow_null=True)
    max_affiliates = serializers.CharField(allow_blank=True, allow_null=True)
    label = serializers.CharField()
    mobile_number = serializers.CharField(allow_blank=True)
    phone_number = serializers.CharField(allow_blank=True)
    code_type = serializers.CharField(allow_blank=True)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField(required=False)
 

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