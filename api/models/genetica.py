# api/models/genetica.py
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, EnumField
from datetime import datetime
from enum import Enum
from .base import BaseDocument, common_indices

class TrasmissioneType(str, Enum):
    AD = "ad"
    AR = "ar"
    X_LINKED = "x_linked"
    MATERNA = "materna"

class GeneTipoType(str, Enum):
    PATOGENETICA = "patogenetica"
    PROB_PATOGENETICA = "prob_patogenetica"
    VUS = "vus"
    PROB_BENIGNA = "prob_benigna"
    BENIGNA = "benigna"

class Gene(EmbeddedDocument):
    nome = StringField(required=True)
    tipo = EnumField(GeneTipoType, required=True)

class Genetica(BaseDocument):
    trasmissione = EnumField(TrasmissioneType, required=True)
    gene = EmbeddedDocumentField(Gene, required=True)

    meta = {
        'collection': 'genetica',
        'indexes': [
            *common_indices,
            ('paziente_id', 'status')
        ]
    }