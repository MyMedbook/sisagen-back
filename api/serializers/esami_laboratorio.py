
# api/serializers/esami_laboratorio.py
from rest_framework import serializers
from .base import BaseSerializer

class BilirubinaSerializer(serializers.Serializer):
    totale = serializers.FloatField(required=True)
    diretta = serializers.FloatField(required=True)
    indiretta = serializers.FloatField(required=True)

    def validate(self, data):
        """Validate that indiretta equals totale minus diretta"""
        if abs(data['totale'] - data['diretta'] - data['indiretta']) > 0.001:
            raise serializers.ValidationError(
                "La bilirubina indiretta deve essere uguale alla differenza tra totale e diretta"
            )
        return data

class EsamiLaboratorioSerializer(BaseSerializer):
    cpk = serializers.FloatField(required=True)
    troponina_hs = serializers.FloatField(required=True)
    nt_pro_bnp = serializers.FloatField(required=True)
    d_dimero = serializers.FloatField(required=True)
    creatinina = serializers.FloatField(required=True)
    azotemia = serializers.FloatField(required=True)
    na = serializers.FloatField(required=True)
    k = serializers.FloatField(required=True)
    gfr = serializers.FloatField(required=True)
    albuminuria = serializers.FloatField(required=True)
    alt = serializers.FloatField(required=True)
    ast = serializers.FloatField(required=True)
    bilirubina = BilirubinaSerializer(required=True)
    ggt = serializers.FloatField(required=True)
    alfa_galattosidasi = serializers.FloatField(required=True)
    componente_monoclonale_sierica = serializers.CharField(required=False, allow_blank=True)
    immunofissazione_sierica = serializers.CharField(required=False, allow_blank=True)
    immunofissazione_urinaria = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        """Add any cross-field validations here"""
        # Example validation: GFR should be between 0 and 200
        if not 0 <= data['gfr'] <= 200:
            raise serializers.ValidationError("GFR deve essere tra 0 e 200")
        return data