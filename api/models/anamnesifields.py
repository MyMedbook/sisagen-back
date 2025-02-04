from mongoengine import (
    EmbeddedDocument, EmbeddedDocumentField, 
    StringField, BooleanField, IntField, ListField, 
    DateTimeField, EnumField
    )
from enum import Enum

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