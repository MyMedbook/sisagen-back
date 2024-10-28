# api/models/anamnesi.py
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, \
    BooleanField, IntField, ListField, DateTimeField, ObjectIdField, EnumField
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    DRAFT = "draft"
    COMPLETE = "complete"
    ARCHIVED = "archived"

class DislipidemiaType(str, Enum):
    NO = "no"
    IPERCOLESTEROLEMIA = "ipercolesterolemia"
    IPERTRIGLICERIDEMIA = "ipertrigliceridemia"
    MISTA = "mista"

class FumoStatus(str, Enum):
    NO = "no"
    SI = "si"
    PASSATO = "passato"

class ObesitaType(str, Enum):
    NORMOPESO = "normopeso"
    SOVRAPPESO = "sovrappeso"
    OBESO = "obeso"

# Embedded Documents for FattoriRischio
class IpertensioneArteriosa(EmbeddedDocument):
    presente = BooleanField(required=True)
    anni = IntField(min_value=0)

class Dislipidemia(EmbeddedDocument):
    tipo = EnumField(DislipidemiaType, required=True)
    anni = IntField(min_value=0)

class DiabeteMellito(EmbeddedDocument):
    presente = BooleanField(required=True)
    anni = IntField(min_value=0)

class Fumo(EmbeddedDocument):
    stato = EnumField(FumoStatus, required=True)
    anni = IntField(min_value=0)
    anni_smesso = IntField(min_value=0)

class FattoriRischio(Document):
    paziente_id = ObjectIdField(required=True)
    operatore_id = ObjectIdField(required=True)
    status = EnumField(Status, default=Status.DRAFT)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    ipertensione_arteriosa = EmbeddedDocumentField(IpertensioneArteriosa)
    dislipidemia = EmbeddedDocumentField(Dislipidemia)
    diabete_mellito = EmbeddedDocumentField(DiabeteMellito)
    fumo = EmbeddedDocumentField(Fumo)
    obesita = EnumField(ObesitaType)

    meta = {
        'collection': 'fattori_rischio',
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at'
        ]
    }

# Embedded Documents for Comorbidita
class MalattiaRenaleCronica(EmbeddedDocument):
    presente = BooleanField(required=True)
    stadio = IntField(min_value=0)

class SteatosiEpatica(EmbeddedDocument):
    presente = BooleanField(required=True)
    grado = StringField()

class Anemia(EmbeddedDocument):
    presente = BooleanField(required=True)
    tipo = StringField()

class DistiroidismoType(str, Enum):
    NO = "no"
    IPOTIROIDISMO = "ipotiroidismo"
    IPERTIROIDISMO = "ipertiroidismo"
    TIROIDECTOMIA = "tiroidectomia"

class Comorbidita(Document):
    paziente_id = ObjectIdField(required=True)
    operatore_id = ObjectIdField(required=True)
    status = EnumField(Status, default=Status.DRAFT)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    malattia_renale_cronica = EmbeddedDocumentField(MalattiaRenaleCronica)
    bpco = BooleanField()
    steatosi_epatica = EmbeddedDocumentField(SteatosiEpatica)
    anemia = EmbeddedDocumentField(Anemia)
    distiroidismo = EnumField(DistiroidismoType)

    meta = {
        'collection': 'comorbidita',
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at'
        ]
    }

# Sintomatologia Models
class DoloreToracicoType(str, Enum):
    TIPICO = "tipico"
    ATIPICO = "atipico"

class FrequenzaType(str, Enum):
    RARO = "raro"
    FREQUENTE = "frequente"

class SincopeType(str, Enum):
    NO = "no"
    LIPOTIMIA = "lipotimia"
    SINCOPE = "sincope"

class VerosimileType(str, Enum):
    VASOVAGALE = "vasovagale"
    ARITMICA = "aritmica"

class DoloreToracico(EmbeddedDocument):
    presente = BooleanField(required=True)
    tipo = EnumField(DoloreToracicoType)
    frequenza = EnumField(FrequenzaType)

class Dispnea(EmbeddedDocument):
    presente = BooleanField(required=True)
    classe_nyha = IntField(min_value=1, max_value=4)

class Cardiopalmo(EmbeddedDocument):
    presente = BooleanField(required=True)
    frequenza = EnumField(FrequenzaType)

class Sincope(EmbeddedDocument):
    tipo = EnumField(SincopeType)
    verosimile = EnumField(VerosimileType)

class Altro(EmbeddedDocument):
    presente = BooleanField(required=True)
    descrizione = StringField()

class Sintomatologia(Document):
    paziente_id = ObjectIdField(required=True)
    operatore_id = ObjectIdField(required=True)
    status = EnumField(Status, default=Status.DRAFT)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    dolore_toracico = EmbeddedDocumentField(DoloreToracico)
    dispnea = EmbeddedDocumentField(Dispnea)
    cardiopalmo = EmbeddedDocumentField(Cardiopalmo)
    sincope = EmbeddedDocumentField(Sincope)
    altro = EmbeddedDocumentField(Altro)

    meta = {
        'collection': 'sintomatologia',
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at'
        ]
    }

# Coinvolgimento Multisistemico Models
class SistemaNervosoType(str, Enum):
    NO = "no"
    DIFFICOLTA_APPRENDIMENTO = "difficolta_apprendimento"
    RITARDO_PSICOMOTORIO = "ritardo_psicomotorio"
    ATASSIA = "atassia"
    PARESTESIE = "parestesie"

class OcchioType(str, Enum):
    NO = "no"
    IPOVISIONE = "ipovisione"
    PTOSI_PALPEBRALE = "ptosi_palpebrale"

class OrecchioType(str, Enum):
    NO = "no"
    DIFFICOLTA_APPRENDIMENTO = "difficolta_apprendimento"
    RITARDO_PSICOMOTORIO = "ritardo_psicomotorio"
    ATASSIA = "atassia"

class SistemaMuscoloscheletricoType(str, Enum):
    NO = "no"
    MIOTONIA = "miotonia"
    TUNNEL_CARPALE_BILATERALE = "tunnel_carpale_bilaterale"
    DEBOLEZZA_MUSCOLARE = "debolezza_muscolare"

class PelleType(str, Enum):
    NO = "no"
    LENTIGGINI = "lentiggini"
    ANGIOCHERATOMA = "angiocheratoma"
    CHERATODERMIA = "cheratodermia"

class CoinvolgimentoMultisistemico(Document):
    paziente_id = ObjectIdField(required=True)
    operatore_id = ObjectIdField(required=True)
    status = EnumField(Status, default=Status.DRAFT)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    sistema_nervoso = EnumField(SistemaNervosoType)
    occhio = EnumField(OcchioType)
    orecchio = EnumField(OrecchioType)
    sistema_muscoloscheletrico = EnumField(SistemaMuscoloscheletricoType)
    pelle = EnumField(PelleType)

    meta = {
        'collection': 'coinvolgimento_multisistemico',
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at'
        ]
    }

# Terapia Farmacologica Model
class TerapiaFarmacologica(Document):
    paziente_id = ObjectIdField(required=True)
    operatore_id = ObjectIdField(required=True)
    status = EnumField(Status, default=Status.DRAFT)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    farmaci = ListField(StringField())

    meta = {
        'collection': 'terapia_farmacologica',
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at'
        ]
    }