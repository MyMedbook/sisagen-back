
# api/models/ecg.py
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, EnumField
from datetime import datetime
from enum import Enum
from .base import BaseDocument

class RitmoType(str, Enum):
    RITMO_SINUSALE = "ritmo_sinusale"
    FA = "fa"
    BESV = "besv"
    BEV = "bev"

class PRType(str, Enum):
    NEI_LIMITI = "nei_limiti"
    BAV_I = "bav_i"
    CORTO_PREECCITAZIONE = "corto_preeccitazione"

class QRSType(str, Enum):
    NEI_LIMITI = "nei_limiti"
    IVS = "ivs"
    ONDE_Q = "onde_q"
    BBD = "bbd"
    BBS = "bbs"
    BASSI_VOLTAGGI = "bassi_voltaggi"

class RVStatoType(str, Enum):
    NEI_LIMITI = "nei_limiti"
    T_NEGATIVE = "t_negative"

class RV(EmbeddedDocument):
    stato = EnumField(RVStatoType, required=True)
    dettagli = StringField(required=False)

class ECG(BaseDocument):
    ritmo = EnumField(RitmoType, required=True)
    pr = EnumField(PRType, required=True)
    qrs = EnumField(QRSType, required=True)
    rv = EmbeddedDocumentField(RV, required=True)

    meta = {
        'collection': 'ecg',
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at',
            ('paziente_id', 'status')
        ]
    }
