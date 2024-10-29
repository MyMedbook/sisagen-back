# api/models/ecocardiogramma.py
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, FloatField
from .base import BaseDocument

class GradientePressorio(EmbeddedDocument):
    medio = FloatField(required=True)
    max = FloatField(required=True)

class Ecocardiogramma(BaseDocument):
    diametro_telediastolico_vs = FloatField(required=True)
    spessore_siv = FloatField(required=True)
    spessore_pp = FloatField(required=True)
    diametro_anteroposteriore_as = FloatField(required=True)
    volume_as = FloatField(required=True)
    radice_aortica = FloatField(required=True)
    aorta_ascendente = FloatField(required=True)
    fe = FloatField(required=True)
    gp_aortico = EmbeddedDocumentField(GradientePressorio, required=True)
    gp_mitralico = EmbeddedDocumentField(GradientePressorio, required=True)
    paps = FloatField(required=True)
    lvot = FloatField(required=True)

    meta = {
        'collection': 'ecocardiogramma',
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at',
            ('paziente_id', 'status')
        ]
    }
