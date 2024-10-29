# api/serializers/pedigree.py
from rest_framework import serializers
from api.models.pedigree import Status, Severita, Device

# Base Serializer
class BaseSerializer(serializers.Serializer):
    """Base serializer with common fields"""
    paziente_id = serializers.IntegerField(required=True)
    operatore_id = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in Status], 
        default=Status.DRAFT
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_paziente_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("paziente_id must be positive")
        return value

    def validate_operatore_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("operatore_id must be positive")
        return value

# Family Member Serializer
class FamilyMemberSerializer(serializers.Serializer):
    """Serializer for family member information"""
    stessa_malattia = serializers.BooleanField(required=True)
    eta_esordio = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    severita = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in Severita],
        required=False,
        allow_null=True
    )
    morte_improvvisa = serializers.BooleanField(required=True)
    eta_morte = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    device = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in Device],
        default=Device.NO
    )

    def validate(self, data):
        """
        Validate related fields
        """
        if data.get('stessa_malattia') and not data.get('eta_esordio'):
            raise serializers.ValidationError(
                "eta_esordio is required when stessa_malattia is True"
            )
        if data.get('morte_improvvisa') and not data.get('eta_morte'):
            raise serializers.ValidationError(
                "eta_morte is required when morte_improvvisa is True"
            )
        return data

# Numbered Family Member Serializer
class NumberedFamilyMemberSerializer(FamilyMemberSerializer):
    """Serializer for numbered family members (fratelli, figli)"""
    numero = serializers.IntegerField(min_value=1, required=True)

# Main Pedigree Serializer
class PedigreeSerializer(BaseSerializer):
    """Main serializer for pedigree information"""
    padre = FamilyMemberSerializer(required=False, allow_null=True)
    madre = FamilyMemberSerializer(required=False, allow_null=True)
    nonno_paterno = FamilyMemberSerializer(required=False, allow_null=True)
    nonna_paterna = FamilyMemberSerializer(required=False, allow_null=True)
    nonno_materno = FamilyMemberSerializer(required=False, allow_null=True)
    nonna_materna = FamilyMemberSerializer(required=False, allow_null=True)
    fratelli = NumberedFamilyMemberSerializer(many=True, required=False)
    figli = NumberedFamilyMemberSerializer(many=True, required=False)

    def validate_numbered_members(self, members):
        """Validate that numbered members have unique numbers"""
        if members:
            numbers = [m['numero'] for m in members]
            if len(numbers) != len(set(numbers)):
                raise serializers.ValidationError("Duplicate numbers found")
        return members

    def validate_fratelli(self, value):
        return self.validate_numbered_members(value)

    def validate_figli(self, value):
        return self.validate_numbered_members(value)