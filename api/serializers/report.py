from rest_framework import serializers
from api.models.report import Report
from .anamnesi import (
    FattoriRischioSer, ComorbiditaSer, SintomatologiaSer,
    CoinvolgimentoMultisistemicoSer, TerapiaFarmacologicaSer
)
from .ecg import ECGSerializer
from .ecocardiogramma import EcocardiogrammaSerializer
from .esami_laboratorio import EsamiLaboratorioSerializer
from .genetica import GeneticaSerializer
from .pedigree import PedigreeSerializer
from .base import BaseSerializer

class QuickReportSerializer(BaseSerializer):
    """
    Serializer for quick report metadata only
    """
    report_id = serializers.IntegerField()
    paziente_nome = serializers.CharField(required=True)
    paziente_cognome = serializers.CharField(required=True)
    operatore_nome = serializers.CharField(required=True)
    operatore_cognome = serializers.CharField(required=True)

class ReportSerializer(BaseSerializer):
    """
    Serializer for the Report model that includes all sections
    """
    report_id = serializers.IntegerField()
    paziente_nome = serializers.CharField(required=True)
    paziente_cognome = serializers.CharField(required=True)
    operatore_nome = serializers.CharField(required=True)
    operatore_cognome = serializers.CharField(required=True)
    
    # All section serializers
    fattori_rischio = FattoriRischioSer()
    comorbidita = ComorbiditaSer()
    sintomatologia = SintomatologiaSer()
    coinvolgimento_multisistemico = CoinvolgimentoMultisistemicoSer()
    terapia_farmacologica = TerapiaFarmacologicaSer()
    ecg = ECGSerializer()
    ecocardiogramma = EcocardiogrammaSerializer()
    esami_laboratorio = EsamiLaboratorioSerializer()
    genetica = GeneticaSerializer()
    pedigree = PedigreeSerializer()