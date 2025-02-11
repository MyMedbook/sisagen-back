from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from api.models.anamnesifields import (
    Altro, Anemia, Cardiopalmo, DiabeteMellito, Dislipidemia, Dispnea, DoloreToracico, 
    Fumo, IpertensioneArteriosa, MalattiaRenaleCronica, Sincope, SteatosiEpatica)
from api.models import (
    FattoriRischio, Comorbidita, Sintomatologia,
    CoinvolgimentoMultisistemico, TerapiaFarmacologica,
   )
from api.serializers import (
    FattoriRischioSer, ComorbiditaSer, SintomatologiaSer,
    CoinvolgimentoMultisistemicoSer, TerapiaFarmacologicaSer,
    AnamnesiCompletaSer
)
from api.views.base import SisagenViewSet


class FattoriRischioViewSet(SisagenViewSet):
     
    model = FattoriRischio
    serializer_class = FattoriRischioSer
    embedded_fields = {
        "ipertensione_arteriosa" : IpertensioneArteriosa,
        "dislipidemia" : Dislipidemia,
        "diabete_mellito" : DiabeteMellito,
        "fumo" : Fumo,
    }


class ComorbiditaViewSet(SisagenViewSet):
     
    model = Comorbidita
    serializer_class = ComorbiditaSer
    embedded_fields = {
        "malattia_renale" : MalattiaRenaleCronica,
        "steatosi_epatica" : SteatosiEpatica,
        "anemia" : Anemia
    }


class SintomatologiaViewSet(SisagenViewSet):
     
    model = Sintomatologia
    serializer_class = SintomatologiaSer
    embedded_fields = {
        "dolore_toracico" : DoloreToracico,
        "dispnea" : Dispnea,
        "cardiopalmo" : Cardiopalmo,
        "sincope" : Sincope,
        "altro" : Altro
    }


class CoinvolgimentoViewSet(SisagenViewSet):
     
    model = CoinvolgimentoMultisistemico
    serializer_class = CoinvolgimentoMultisistemicoSer
    embedded_fields = {}


class TerapiaViewSet(SisagenViewSet):
     
    model = TerapiaFarmacologica
    serializer_class = TerapiaFarmacologicaSer
    embedded_fields = {}


class AnamnesiCompletaView(APIView):
    """View for handling complete anamnesis records"""
    
    def _get_latest(self, model, serializer, patient_id):

        obj = model.objects(paziente_id=patient_id).order_by('-created_at').first()
        if not obj:
            return None
        
        return serializer(obj).data
        
    def _get_all_records(self, patient_id):
        """Helper method to fetch all anamnesis records with consistent key names"""
        records = {
            'fattori_rischio': self._get_latest(FattoriRischio, FattoriRischioSer, patient_id),
            'comorbidita': self._get_latest(Comorbidita, ComorbiditaSer, patient_id),
            'sintomatologia': self._get_latest(Sintomatologia, SintomatologiaSer, patient_id),
            'coinvolgimento_multisistemico': self._get_latest(CoinvolgimentoMultisistemico, CoinvolgimentoMultisistemicoSer, patient_id),
            'terapia_farmacologica': self._get_latest(TerapiaFarmacologica, TerapiaFarmacologicaSer, patient_id)
        }

        if all(v is None for v in records.values()):
            raise NotFound(f"No Anamnesi records found for patient with id {patient_id}")
        
        return records

    def get(self, request, paziente_id):
        """Get complete anamnesis record with available sections"""

        records = self._get_all_records(paziente_id)

        created_at = min(record["created_at"] for record in records.values() if not record is None)
        updated_at = max(record["updated_at"] for record in records.values() if not record is None)

        data = {
            'paziente_id': paziente_id,
            'created_at': created_at,
            'updated_at': updated_at
        }

        data.update(records)

        # Add information about missing sections
        missing_sections = [k for k, v in records.items() if v is None]

        response_data = {
            "message": "Partial data available" if missing_sections else "Complete data available",
            "data": data
        }

        # Only include missing_sections in response if there are any
        if missing_sections:
            response_data["missing_sections"] = missing_sections

        return Response(response_data)
