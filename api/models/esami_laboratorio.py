# api/models/esami_laboratorio.py
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, FloatField, StringField
from .base import BaseDocument

class Bilirubina(EmbeddedDocument):
    totale = FloatField(required=True)
    diretta = FloatField(required=True)
    indiretta = FloatField(required=True)

class EsamiLaboratorio(BaseDocument):
    cpk = FloatField(required=True)
    troponina_hs = FloatField(required=True)
    nt_pro_bnp = FloatField(required=True)
    d_dimero = FloatField(required=True)
    creatinina = FloatField(required=True)
    azotemia = FloatField(required=True)
    na = FloatField(required=True)
    k = FloatField(required=True)
    gfr = FloatField(required=True)
    albuminuria = FloatField(required=True)
    alt = FloatField(required=True)
    ast = FloatField(required=True)
    bilirubina = EmbeddedDocumentField(Bilirubina, required=True)
    ggt = FloatField(required=True)
    alfa_galattosidasi = FloatField(required=True)
    componente_monoclonale_sierica = StringField()
    immunofissazione_sierica = StringField()
    immunofissazione_urinaria = StringField()

    meta = {
        'collection': 'esami_laboratorio',
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at',
            ('paziente_id', 'status')
        ]
    }
