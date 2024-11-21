from mongoengine import (
    Document, EmbeddedDocument, EmbeddedDocumentField, 
    StringField, IntField, DateTimeField, DictField,
    ListField, ReferenceField
)
from datetime import datetime
from .base import BaseDocument
from .anamnesi import (
    FattoriRischio, Comorbidita, Sintomatologia,
    CoinvolgimentoMultisistemico, TerapiaFarmacologica
)
from .ecg import ECG
from .ecocardiogramma import Ecocardiogramma
from .esami_laboratorio import EsamiLaboratorio
from .genetica import Genetica
from .pedigree import Pedigree

class Report(BaseDocument):
    """
    Report model that collects the latest values from all sections
    """
    report_id = IntField(required=True)  # Sequential report ID per patient
    paziente_nome = StringField(required=True)
    paziente_cognome = StringField(required=True)
    operatore_nome = StringField(required=True)
    operatore_cognome = StringField(required=True)
    
    # References to the actual documents
    fattori_rischio = ReferenceField(FattoriRischio)
    comorbidita = ReferenceField(Comorbidita)
    sintomatologia = ReferenceField(Sintomatologia)
    coinvolgimento_multisistemico = ReferenceField(CoinvolgimentoMultisistemico)
    terapia_farmacologica = ReferenceField(TerapiaFarmacologica)
    ecg = ReferenceField(ECG)
    ecocardiogramma = ReferenceField(Ecocardiogramma)
    esami_laboratorio = ReferenceField(EsamiLaboratorio)
    genetica = ReferenceField(Genetica)
    pedigree = ReferenceField(Pedigree)

    meta = {
        'collection': 'reports',
        'indexes': [
            'paziente_id',
            'report_id',
            ('paziente_id', 'report_id'),
            'created_at'
        ]
    }

    @classmethod
    def get_next_report_id(cls, paziente_id):
        """Get the next sequential report ID for a patient"""
        last_report = cls.objects(paziente_id=paziente_id).order_by('-report_id').first()
        return (last_report.report_id + 1) if last_report else 1

    def get_latest_records(self):
        """Get the latest records for all sections"""
        pid = self.paziente_id
        return {
            'fattori_rischio': FattoriRischio.objects(paziente_id=pid).order_by('-created_at').first(),
            'comorbidita': Comorbidita.objects(paziente_id=pid).order_by('-created_at').first(),
            'sintomatologia': Sintomatologia.objects(paziente_id=pid).order_by('-created_at').first(),
            'coinvolgimento_multisistemico': CoinvolgimentoMultisistemico.objects(paziente_id=pid).order_by('-created_at').first(),
            'terapia_farmacologica': TerapiaFarmacologica.objects(paziente_id=pid).order_by('-created_at').first(),
            'ecg': ECG.objects(paziente_id=pid).order_by('-created_at').first(),
            'ecocardiogramma': Ecocardiogramma.objects(paziente_id=pid).order_by('-created_at').first(),
            'esami_laboratorio': EsamiLaboratorio.objects(paziente_id=pid).order_by('-created_at').first(),
            'genetica': Genetica.objects(paziente_id=pid).order_by('-created_at').first(),
            'pedigree': Pedigree.objects(paziente_id=pid).order_by('-created_at').first()
        }