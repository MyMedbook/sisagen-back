# api/serializers/ecocardiogramma.py
from rest_framework import serializers
from .base import BaseSerializer

class GradientePressorioSerializer(serializers.Serializer):
    medio = serializers.FloatField(required=True)
    max = serializers.FloatField(required=True)

    def validate(self, data):
        """Validate that max is greater than medio"""
        if data['max'] <= data['medio']:
            raise serializers.ValidationError(
                "Il gradiente massimo deve essere maggiore del gradiente medio"
            )
        return data

class EcocardiogrammaSerializer(BaseSerializer):
    diametro_telediastolico_vs = serializers.FloatField(required=True)
    spessore_siv = serializers.FloatField(required=True)
    spessore_pp = serializers.FloatField(required=True)
    diametro_anteroposteriore_as = serializers.FloatField(required=True)
    volume_as = serializers.FloatField(required=True)
    radice_aortica = serializers.FloatField(required=True)
    aorta_ascendente = serializers.FloatField(required=True)
    fe = serializers.FloatField(required=True)
    gp_aortico = GradientePressorioSerializer(required=True)
    gp_mitralico = GradientePressorioSerializer(required=True)
    paps = serializers.FloatField(required=True)
    lvot = serializers.FloatField(required=True)

    def validate_fe(self, value):
        """Validate fraction ejection is between 0 and 100"""
        if not 0 <= value <= 100:
            raise serializers.ValidationError("FE deve essere tra 0 e 100")
        return value