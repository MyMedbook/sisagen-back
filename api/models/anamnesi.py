from mongoengine import (
    Document, EmbeddedDocument, EmbeddedDocumentField, 
    StringField, BooleanField, IntField, ListField, 
    DateTimeField, EnumField
)
from datetime import datetime
from enum import Enum
from .base import BaseDocument
import api.models.anamnesifields as af


# Main Document Classes
class FattoriRischio(BaseDocument):
    ipertensione_arteriosa = EmbeddedDocumentField(af.IpertensioneArteriosa)
    dislipidemia = EmbeddedDocumentField(af.Dislipidemia)
    diabete_mellito = EmbeddedDocumentField(af.DiabeteMellito)
    fumo = EmbeddedDocumentField(af.Fumo)
    obesita = EnumField(af.ObesitaType)

    meta = {'collection': 'fattori_rischio'}

class Comorbidita(BaseDocument):
    malattia_renale = EmbeddedDocumentField(af.MalattiaRenaleCronica)
    bpco = BooleanField()
    steatosi_epatica = EmbeddedDocumentField(af.SteatosiEpatica)
    anemia = EmbeddedDocumentField(af.Anemia)
    distiroidismo = EnumField(af.DistiroidismoType)

    meta = {'collection': 'comorbidita'}

class Sintomatologia(BaseDocument):
    dolore_toracico = EmbeddedDocumentField(af.DoloreToracico)
    dispnea = EmbeddedDocumentField(af.Dispnea)
    cardiopalmo = EmbeddedDocumentField(af.Cardiopalmo)
    sincope = EmbeddedDocumentField(af.Sincope)
    altro = EmbeddedDocumentField(af.Altro)

    meta = {'collection': 'sintomatologia'}

class CoinvolgimentoMultisistemico(BaseDocument):
    sistema_nervoso = EnumField(af.SistemaNervosoType)
    occhio = EnumField(af.OcchioType)
    orecchio = EnumField(af.OrecchioType)
    sistema_muscoloscheletrico = EnumField(af.SistemaMuscoloscheletricoType)
    pelle = EnumField(af.PelleType)

    meta = {'collection': 'coinvolgimento_multisistemico'}

class TerapiaFarmacologica(BaseDocument):
    farmaci = ListField(StringField())

    meta = {'collection': 'terapia_farmacologica'}