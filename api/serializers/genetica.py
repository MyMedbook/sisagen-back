# api/serializers/genetica.py
from rest_framework import serializers
from api.models.genetica import TrasmissioneType, GeneTipoType
from .base import BaseSerializer

class GeneSerializer(serializers.Serializer):
    nome = serializers.CharField(required=True)
    tipo = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in GeneTipoType],
        required=True
    )

class GeneticaSerializer(BaseSerializer):
    trasmissione = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in TrasmissioneType],
        required=True
    )
    gene = GeneSerializer(required=True)