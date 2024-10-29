from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from datetime import datetime
import logging

from api.models import (
    FattoriRischio, Comorbidita, Sintomatologia,
    CoinvolgimentoMultisistemico, TerapiaFarmacologica
)
from api.serializers import (
    FattoriRischioSer, ComorbiditaSer, SintomatologiaSer,
    CoinvolgimentoMultisistemicoSer, TerapiaFarmacologicaSer,
    AnamnesiCompletaSer
)

logger = logging.getLogger(__name__)

class BaseAnamnesisView(APIView):
    """Base view for handling anamnesis records"""
    model = None
    serializer_class = None

    def validate_paziente_id(self, paziente_id):
        """Validate and convert paziente_id to integer"""
        try:
            pid = int(paziente_id)
            if pid <= 0:
                raise ValidationError("paziente_id must be positive")
            return pid
        except ValueError:
            raise ValidationError("paziente_id must be a valid integer")

    def get_object(self, paziente_id):
        """Get object with validated paziente_id"""
        pid = self.validate_paziente_id(paziente_id)
        try:
            return self.model.objects(paziente_id=pid).first()
        except Exception as e:
            logger.error(f"Error fetching {self.model.__name__}: {str(e)}")
            raise

    def check_exists(self, paziente_id):
        """Check if record exists for patient"""
        return self.model.objects(paziente_id=paziente_id).count() > 0

    def get(self, request, paziente_id):
        """Get anamnesis record"""
        try:
            instance = self.get_object(paziente_id)
            if not instance:
                raise NotFound(f"{self.model.__name__} not found for patient {paziente_id}")
                
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        except (ValidationError, NotFound) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in GET: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, paziente_id):
        """Create new anamnesis record"""
        try:
            pid = self.validate_paziente_id(paziente_id)
            
            # Check if record already exists using MongoEngine syntax
            if self.check_exists(pid):
                return Response(
                    {"error": f"{self.model.__name__} already exists for this patient"},
                    status=status.HTTP_409_CONFLICT
                )
            
            # Prepare data
            data = request.data.copy()
            data['paziente_id'] = pid
            
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Create and save instance
            instance = self.model(**serializer.validated_data)
            instance.save()
            
            return Response(
                self.serializer_class(instance).data, 
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in POST: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, paziente_id):
        """Update existing anamnesis record"""
        try:
            instance = self.get_object(paziente_id)
            if not instance:
                raise NotFound(f"{self.model.__name__} not found for patient {paziente_id}")
            
            # Prepare data
            data = request.data.copy()
            data['paziente_id'] = instance.paziente_id
            
            serializer = self.serializer_class(instance, data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Update instance
            for key, value in serializer.validated_data.items():
                setattr(instance, key, value)
            instance.updated_at = datetime.utcnow()
            instance.save()
            
            return Response(self.serializer_class(instance).data)
        except (ValidationError, NotFound) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in PUT: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, paziente_id):
        """Delete anamnesis record"""
        try:
            instance = self.get_object(paziente_id)
            if not instance:
                raise NotFound(f"{self.model.__name__} not found for patient {paziente_id}")
            
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (ValidationError, NotFound) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in DELETE: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AnamnesiCompletaView(APIView):
    """View for handling complete anamnesis records"""
    
    def _get_all_records(self, patient_id):
        """Helper method to fetch all anamnesis records"""
        records = {
            'fattori_rischio': FattoriRischio.objects(paziente_id=patient_id).first(),
            'comorbidita': Comorbidita.objects(paziente_id=patient_id).first(),
            'sintomatologia': Sintomatologia.objects(paziente_id=patient_id).first(),
            'coinvolgimento': CoinvolgimentoMultisistemico.objects(paziente_id=patient_id).first(),
            'terapia': TerapiaFarmacologica.objects(paziente_id=patient_id).first()
        }
        
        # Check if any record is missing
        missing = [k for k, v in records.items() if v is None]
        if missing:
            raise NotFound(f"Missing records for: {', '.join(missing)}")
            
        return records

    def get(self, request, paziente_id):
        """Get complete anamnesis record"""
        try:
            patient_id = self.validate_paziente_id(paziente_id)
            records = self._get_all_records(patient_id)

            data = {
                'paziente_id': patient_id,
                'operatore_id': records['fattori_rischio'].operatore_id,
                'created_at': records['fattori_rischio'].created_at,
                'updated_at': max(r.updated_at for r in records.values()),
                'fattori_rischio': FattoriRischioSer(records['fattori_rischio']).data,
                'comorbidita': ComorbiditaSer(records['comorbidita']).data,
                'sintomatologia': SintomatologiaSer(records['sintomatologia']).data,
                'coinvolgimento_multisistemico': CoinvolgimentoMultisistemicoSer(records['coinvolgimento']).data,
                'terapia_farmacologica': TerapiaFarmacologicaSer(records['terapia']).data
            }

            serializer = AnamnesiCompletaSer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AnamnesiCompleta GET: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Concrete view classes remain the same
class FattoriRischioView(BaseAnamnesisView):
    model = FattoriRischio
    serializer_class = FattoriRischioSer

class ComorbiditaView(BaseAnamnesisView):
    model = Comorbidita
    serializer_class = ComorbiditaSer

class SintomatologiaView(BaseAnamnesisView):
    model = Sintomatologia
    serializer_class = SintomatologiaSer

class CoinvolgimentoMultisistemicoView(BaseAnamnesisView):
    model = CoinvolgimentoMultisistemico
    serializer_class = CoinvolgimentoMultisistemicoSer

class TerapiaFarmacologicaView(BaseAnamnesisView):
    model = TerapiaFarmacologica
    serializer_class = TerapiaFarmacologicaSer