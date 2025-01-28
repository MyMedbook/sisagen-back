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
from api.views.base import SisagenViewSet, to_json


class AnamnesiViewSet(SisagenViewSet):

    embedded_fields = {}

    def create(self, request):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        validated_data = serializer.validated_data
        for key, field_model in self.embedded_fields.items():
            validated_data[key] = field_model(**validated_data[key])

        instance = self.model(**validated_data)
        instance.save()

        return Response(
            to_json(instance),
            status.HTTP_201_CREATED
                )


class FattoriRischioViewSet(AnamnesiViewSet):
     
    model = FattoriRischio
    serializer_class = FattoriRischioSer
    embedded_fields = {
        "ipertensione_arteriosa" : IpertensioneArteriosa,
        "dislipidemia" : Dislipidemia,
        "diabete_mellito" : DiabeteMellito,
        "fumo" : Fumo,
    }


class ComorbiditaViewSet(AnamnesiViewSet):
     
    model = Comorbidita
    serializer_class = ComorbiditaSer
    embedded_fields = {
        "malattia_renale_cronica" : MalattiaRenaleCronica,
        "steatosi_epatica" : SteatosiEpatica,
        "anemia" : Anemia
    }


class SintomatologiaViewSet(AnamnesiViewSet):
     
    model = Sintomatologia
    serializer_class = SintomatologiaSer
    embedded_fields = {
        "dolore_toracico" : DoloreToracico,
        "dispnea" : Dispnea,
        "cardiopalmo" : Cardiopalmo,
        "sincope" : Sincope,
        "altro" : Altro
    }


class CoinvolgimentoViewSet(AnamnesiViewSet):
     
    model = CoinvolgimentoMultisistemico
    serializer_class = CoinvolgimentoMultisistemicoSer
    embedded_fields = {}


class TerapiaViewSet(AnamnesiViewSet):
     
    model = TerapiaFarmacologica
    serializer_class = TerapiaFarmacologicaSer
    embedded_fields = {}


class AnamnesiCompletaNuView(APIView):
    """View for handling complete anamnesis records"""
    
    def _get_latest(self, model, patient_id):

        obj = model.objects(paziente_id=patient_id).order_by('-created_at').first()
        if not obj:
            return None
        
        return to_json(obj)
        
    def _get_all_records(self, patient_id):
        """Helper method to fetch all anamnesis records with consistent key names"""
        records = {
            'fattori_rischio': self._get_latest(FattoriRischio, patient_id),
            'comorbidita': self._get_latest(Comorbidita, patient_id),
            'sintomatologia': self._get_latest(Sintomatologia, patient_id),
            'coinvolgimento_multisistemico': self._get_latest(CoinvolgimentoMultisistemico, patient_id),
            'terapia_farmacologica': self._get_latest(TerapiaFarmacologica, patient_id)
        }

        if all(v is None for v in records.values()):
            raise NotFound(f"No Anamnesi records found for patient with id {patient_id}")
        
        return records

    def get(self, request, paziente_id):
        """Get complete anamnesis record with available sections"""

        records = self._get_all_records(paziente_id)

        created_at = min(record["created_at"]["$date"] for record in records.values() if not record is None)
        updated_at = max(record["updated_at"]["$date"] for record in records.values() if not record is None)

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
