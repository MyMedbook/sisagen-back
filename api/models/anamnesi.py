from mongoengine import (
    Document, EmbeddedDocument, EmbeddedDocumentField, 
    StringField, BooleanField, IntField, ListField, 
    DateTimeField, EnumField
)
from datetime import datetime
from enum import Enum
from .base import common_indices

# Status Enums
class Status(str, Enum):
    DRAFT = "draft"
    COMPLETE = "complete"
    ARCHIVED = "archived"

# Disease Type Enums
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

class DistiroidismoType(str, Enum):
    NO = "no"
    IPOTIROIDISMO = "ipotiroidismo"
    IPERTIROIDISMO = "ipertiroidismo"
    TIROIDECTOMIA = "tiroidectomia"

# Symptom Type Enums
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

# System Involvement Enums
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

# Base Document
class BaseDocument(Document):
    """Base document class with common fields and metadata"""
    paziente_id = IntField(required=True)
    operatore_id = IntField(required=True)
    datamanager_id = IntField()
    struttura = StringField()
    status = EnumField(Status, default=Status.DRAFT)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'abstract': True,
        'indexes': common_indices
    }

    def save(self, *args, **kwargs):
        """Update updated_at timestamp on every save"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

    def validate_patient(self):
        """Validate paziente_id"""
        if self.paziente_id <= 0:
            raise ValueError("paziente_id must be positive")

    def clean(self):
        """Perform document validation before saving"""
        self.validate_patient()
        super().clean()

# Embedded Documents for FattoriRischio
class IpertensioneArteriosa(EmbeddedDocument):
    presente = BooleanField(required=True)
    anno_insorgenza = IntField(min_value=0)
    anni = IntField(min_value=0)

class Dislipidemia(EmbeddedDocument):
    tipo = EnumField(DislipidemiaType, required=True)
    anno_insorgenza = IntField(min_value=0)
    anni = IntField(min_value=0)

class DiabeteMellito(EmbeddedDocument):
    presente = BooleanField(required=True)
    anno_insorgenza = IntField(min_value=0)
    anni = IntField(min_value=0)

class Fumo(EmbeddedDocument):
    stato = EnumField(FumoStatus, required=True)
    anno_inizio = IntField(min_value=0)
    anno_interruzione = IntField(min_value=0)
    anni = IntField(min_value=0)
    anni_smesso = IntField(min_value=0)

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

# Embedded Documents for Sintomatologia
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

# Main Document Classes
class FattoriRischio(BaseDocument):
    ipertensione_arteriosa = EmbeddedDocumentField(IpertensioneArteriosa)
    dislipidemia = EmbeddedDocumentField(Dislipidemia)
    diabete_mellito = EmbeddedDocumentField(DiabeteMellito)
    fumo = EmbeddedDocumentField(Fumo)
    obesita = EnumField(ObesitaType)

    meta = {'collection': 'fattori_rischio'}

class Comorbidita(BaseDocument):
    malattia_renale_cronica = EmbeddedDocumentField(MalattiaRenaleCronica)
    bpco = BooleanField()
    steatosi_epatica = EmbeddedDocumentField(SteatosiEpatica)
    anemia = EmbeddedDocumentField(Anemia)
    distiroidismo = EnumField(DistiroidismoType)

    meta = {'collection': 'comorbidita'}

class Sintomatologia(BaseDocument):
    dolore_toracico = EmbeddedDocumentField(DoloreToracico)
    dispnea = EmbeddedDocumentField(Dispnea)
    cardiopalmo = EmbeddedDocumentField(Cardiopalmo)
    sincope = EmbeddedDocumentField(Sincope)
    altro = EmbeddedDocumentField(Altro)

    meta = {'collection': 'sintomatologia'}

class CoinvolgimentoMultisistemico(BaseDocument):
    sistema_nervoso = EnumField(SistemaNervosoType)
    occhio = EnumField(OcchioType)
    orecchio = EnumField(OrecchioType)
    sistema_muscoloscheletrico = EnumField(SistemaMuscoloscheletricoType)
    pelle = EnumField(PelleType)

    meta = {'collection': 'coinvolgimento_multisistemico'}

class TerapiaFarmacologica(BaseDocument):
    farmaci = ListField(StringField())

    meta = {'collection': 'terapia_farmacologica'}