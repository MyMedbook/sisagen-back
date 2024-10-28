# api/serializers/anamnesi.py
from rest_framework import serializers
from api.models import (
    Status, DislipidemiaType, FumoStatus, ObesitaType,
    DistiroidismoType, DoloreToracicoType, FrequenzaType,
    SincopeType, VerosimileType, SistemaNervosoType,
    OcchioType, OrecchioType, SistemaMuscoloscheletricoType,
    PelleType
)

# Fattori Rischio Serializers
class IpertensioneArteriosaSer(serializers.Serializer):
    presente = serializers.BooleanField(required=True)
    anni = serializers.IntegerField(min_value=0, required=False)

class DislipidemiaSer(serializers.Serializer):
    tipo = serializers.ChoiceField(choices=[(x.value, x.value) for x in DislipidemiaType])
    anni = serializers.IntegerField(min_value=0, required=False)

class DiabeteMellitoSer(serializers.Serializer):
    presente = serializers.BooleanField(required=True)
    anni = serializers.IntegerField(min_value=0, required=False)

class FumoSer(serializers.Serializer):
    stato = serializers.ChoiceField(choices=[(x.value, x.value) for x in FumoStatus])
    anni = serializers.IntegerField(min_value=0, required=False)
    anni_smesso = serializers.IntegerField(min_value=0, required=False)

class FattoriRischioSer(serializers.Serializer):
    paziente_id = serializers.CharField(required=True)
    operatore_id = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=[(x.value, x.value) for x in Status], default=Status.DRAFT)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    ipertensione_arteriosa = IpertensioneArteriosaSer()
    dislipidemia = DislipidemiaSer()
    diabete_mellito = DiabeteMellitoSer()
    fumo = FumoSer()
    obesita = serializers.ChoiceField(choices=[(x.value, x.value) for x in ObesitaType])

# Comorbidita Serializers
class MalattiaRenaleCronicaSer(serializers.Serializer):
    presente = serializers.BooleanField(required=True)
    stadio = serializers.IntegerField(min_value=0, required=False)

class SteatosiEpaticaSer(serializers.Serializer):
    presente = serializers.BooleanField(required=True)
    grado = serializers.CharField(required=False)

class AnemiaSer(serializers.Serializer):
    presente = serializers.BooleanField(required=True)
    tipo = serializers.CharField(required=False)

class ComorbiditaSer(serializers.Serializer):
    paziente_id = serializers.CharField(required=True)
    operatore_id = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=[(x.value, x.value) for x in Status], default=Status.DRAFT)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    malattia_renale_cronica = MalattiaRenaleCronicaSer()
    bpco = serializers.BooleanField()
    steatosi_epatica = SteatosiEpaticaSer()
    anemia = AnemiaSer()
    distiroidismo = serializers.ChoiceField(choices=[(x.value, x.value) for x in DistiroidismoType])

# Sintomatologia Serializers
class DoloreToracicoSer(serializers.Serializer):
    presente = serializers.BooleanField(required=True)
    tipo = serializers.ChoiceField(choices=[(x.value, x.value) for x in DoloreToracicoType], required=False)
    frequenza = serializers.ChoiceField(choices=[(x.value, x.value) for x in FrequenzaType], required=False)

class DispneaSer(serializers.Serializer):
    presente = serializers.BooleanField(required=True)
    classe_nyha = serializers.IntegerField(min_value=1, max_value=4, required=False)

class CardiopalmoSer(serializers.Serializer):
    presente = serializers.BooleanField(required=True)
    frequenza = serializers.ChoiceField(choices=[(x.value, x.value) for x in FrequenzaType], required=False)

class SincopeSer(serializers.Serializer):
    tipo = serializers.ChoiceField(choices=[(x.value, x.value) for x in SincopeType])
    verosimile = serializers.ChoiceField(choices=[(x.value, x.value) for x in VerosimileType], required=False)

class AltroSer(serializers.Serializer):
    presente = serializers.BooleanField(required=True)
    descrizione = serializers.CharField(required=False)

class SintomatologiaSer(serializers.Serializer):
    paziente_id = serializers.CharField(required=True)
    operatore_id = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=[(x.value, x.value) for x in Status], default=Status.DRAFT)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    dolore_toracico = DoloreToracicoSer()
    dispnea = DispneaSer()
    cardiopalmo = CardiopalmoSer()
    sincope = SincopeSer()
    altro = AltroSer()

# Coinvolgimento Multisistemico Serializer
class CoinvolgimentoMultisistemicoSer(serializers.Serializer):
    paziente_id = serializers.CharField(required=True)
    operatore_id = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=[(x.value, x.value) for x in Status], default=Status.DRAFT)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    sistema_nervoso = serializers.ChoiceField(choices=[(x.value, x.value) for x in SistemaNervosoType])
    occhio = serializers.ChoiceField(choices=[(x.value, x.value) for x in OcchioType])
    orecchio = serializers.ChoiceField(choices=[(x.value, x.value) for x in OrecchioType])
    sistema_muscoloscheletrico = serializers.ChoiceField(choices=[(x.value, x.value) for x in SistemaMuscoloscheletricoType])
    pelle = serializers.ChoiceField(choices=[(x.value, x.value) for x in PelleType])

# Terapia Farmacologica Serializer
class TerapiaFarmacologicaSer(serializers.Serializer):
    paziente_id = serializers.CharField(required=True)
    operatore_id = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=[(x.value, x.value) for x in Status], default=Status.DRAFT)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    farmaci = serializers.ListField(child=serializers.CharField())

# Combined Anamnesi Serializer for GET /anamnesi/
class AnamnesiCompletaSer(serializers.Serializer):
    paziente_id = serializers.CharField(required=True)
    operatore_id = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    fattori_rischio = FattoriRischioSer()
    comorbidita = ComorbiditaSer()
    sintomatologia = SintomatologiaSer()
    coinvolgimento_multisistemico = CoinvolgimentoMultisistemicoSer()
    terapia_farmacologica = TerapiaFarmacologicaSer()