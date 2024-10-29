# api/serializers/ecg.py
from rest_framework import serializers
from api.models.ecg import RitmoType, PRType, QRSType, RVStatoType
from .base import BaseSerializer

class RVSerializer(serializers.Serializer):
    stato = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in RVStatoType],
        required=True
    )
    dettagli = serializers.CharField(required=False, allow_blank=True)

class ECGSerializer(BaseSerializer):
    ritmo = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in RitmoType],
        required=True
    )
    pr = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in PRType],
        required=True
    )
    qrs = serializers.ChoiceField(
        choices=[(x.value, x.value) for x in QRSType],
        required=True
    )
    rv = RVSerializer(required=True)
