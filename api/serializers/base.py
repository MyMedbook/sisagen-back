# api/serializers/base.py
from rest_framework import serializers
from api.models.base import Status

class BaseSerializer(serializers.Serializer):
    """Base serializer with common fields"""
    paziente_id = serializers.IntegerField(required=True)
    operatore_id = serializers.IntegerField(required=True)
    datamanager_id = serializers.IntegerField(required=False, allow_null=True)
    struttura = serializers.CharField(required=False, allow_null=True)
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
