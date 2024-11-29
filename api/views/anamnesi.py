from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from datetime import datetime
import logging

from api.models.anamnesi import Altro, Anemia, Cardiopalmo, DiabeteMellito, Dislipidemia, Dispnea, DoloreToracico, Fumo, IpertensioneArteriosa, MalattiaRenaleCronica, Sincope, SteatosiEpatica
from api.models import (
    FattoriRischio, Comorbidita, Sintomatologia,
    CoinvolgimentoMultisistemico, TerapiaFarmacologica,
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

    def put(self, request, paziente_id):
        """Create or update anamnesis record"""
        try:
            pid = self.validate_paziente_id(paziente_id)
            
            # Prepare data
            data = request.data.copy()
            data['paziente_id'] = pid
            
            # Validate data with serializer
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            instance = self.get_object(pid)
            
            if instance:
                # Update existing record
                if isinstance(instance, FattoriRischio):
                    instance.ipertensione_arteriosa = IpertensioneArteriosa(**validated_data['ipertensione_arteriosa'])
                    instance.dislipidemia = Dislipidemia(**validated_data['dislipidemia'])
                    instance.diabete_mellito = DiabeteMellito(**validated_data['diabete_mellito'])
                    instance.fumo = Fumo(**validated_data['fumo'])
                    instance.obesita = validated_data['obesita']
                
                elif isinstance(instance, Comorbidita):
                    instance.malattia_renale_cronica = MalattiaRenaleCronica(**validated_data['malattia_renale_cronica'])
                    instance.bpco = validated_data['bpco']
                    instance.steatosi_epatica = SteatosiEpatica(**validated_data['steatosi_epatica'])
                    instance.anemia = Anemia(**validated_data['anemia'])
                    instance.distiroidismo = validated_data['distiroidismo']
                
                elif isinstance(instance, Sintomatologia):
                    instance.dolore_toracico = DoloreToracico(**validated_data['dolore_toracico'])
                    instance.dispnea = Dispnea(**validated_data['dispnea'])
                    instance.cardiopalmo = Cardiopalmo(**validated_data['cardiopalmo'])
                    instance.sincope = Sincope(**validated_data['sincope'])
                    instance.altro = Altro(**validated_data['altro'])
                
                elif isinstance(instance, CoinvolgimentoMultisistemico):
                    instance.sistema_nervoso = validated_data['sistema_nervoso']
                    instance.occhio = validated_data['occhio']
                    instance.orecchio = validated_data['orecchio']
                    instance.sistema_muscoloscheletrico = validated_data['sistema_muscoloscheletrico']
                    instance.pelle = validated_data['pelle']
                
                elif isinstance(instance, TerapiaFarmacologica):
                    instance.farmaci = validated_data['farmaci']

                # Update common fields
                instance.operatore_id = validated_data['operatore_id']
                try:
                    instance.datamanager_id = validated_data['datamanager_id']
                except KeyError:
                    pass
                
                instance.status = validated_data['status']
                instance.updated_at = datetime.utcnow()
                
                instance.save()
                response_status = status.HTTP_200_OK
            else:
                common_args = dict(
                    paziente_id=pid,
                    operatore_id=validated_data['operatore_id'],
                    status=validated_data['status']
                )
                try:
                    common_args['datamanager_id'] =  validated_data['datamanager_id']
                except KeyError:
                    pass

                # Create new instance based on model type
                if self.model == FattoriRischio:
                    instance = FattoriRischio(
                        **common_args,
                        ipertensione_arteriosa=IpertensioneArteriosa(**validated_data['ipertensione_arteriosa']),
                        dislipidemia=Dislipidemia(**validated_data['dislipidemia']),
                        diabete_mellito=DiabeteMellito(**validated_data['diabete_mellito']),
                        fumo=Fumo(**validated_data['fumo']),
                        obesita=validated_data['obesita']
                    )
                elif self.model == Comorbidita:
                    instance = Comorbidita(
                        **common_args,
                        malattia_renale_cronica=MalattiaRenaleCronica(**validated_data['malattia_renale_cronica']),
                        bpco=validated_data['bpco'],
                        steatosi_epatica=SteatosiEpatica(**validated_data['steatosi_epatica']),
                        anemia=Anemia(**validated_data['anemia']),
                        distiroidismo=validated_data['distiroidismo']
                    )
                elif self.model == Sintomatologia:
                    instance = Sintomatologia(
                        **common_args,
                        dolore_toracico=DoloreToracico(**validated_data['dolore_toracico']),
                        dispnea=Dispnea(**validated_data['dispnea']),
                        cardiopalmo=Cardiopalmo(**validated_data['cardiopalmo']),
                        sincope=Sincope(**validated_data['sincope']),
                        altro=Altro(**validated_data['altro'])
                    )
                elif self.model == CoinvolgimentoMultisistemico:
                    instance = CoinvolgimentoMultisistemico(
                        **common_args,
                        sistema_nervoso=validated_data['sistema_nervoso'],
                        occhio=validated_data['occhio'],
                        orecchio=validated_data['orecchio'],
                        sistema_muscoloscheletrico=validated_data['sistema_muscoloscheletrico'],
                        pelle=validated_data['pelle']
                    )
                elif self.model == TerapiaFarmacologica:
                    instance = TerapiaFarmacologica(
                        **common_args,
                        farmaci=validated_data['farmaci']
                    )
                
                instance.save()
                response_status = status.HTTP_201_CREATED
            
            return Response(self.serializer_class(instance).data, status=response_status)
            
        except ValidationError as e:
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
            return Response({"result": f"{self.model.__name__} for patient {paziente_id} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except (ValidationError, NotFound) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in DELETE: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Concrete view classes
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

class AnamnesiCompletaView(APIView):
    """View for handling complete anamnesis records"""
    
    def validate_paziente_id(self, paziente_id):
        """Validate and convert paziente_id to integer"""
        try:
            pid = int(paziente_id)
            if pid <= 0:
                raise ValidationError("paziente_id must be positive")
            return pid
        except ValueError:
            raise ValidationError("paziente_id must be a valid integer")
        
    def _get_all_records(self, patient_id):
        """Helper method to fetch all anamnesis records with consistent key names"""
        records = {
            'fattori_rischio': FattoriRischio.objects(paziente_id=patient_id).first(),
            'comorbidita': Comorbidita.objects(paziente_id=patient_id).first(),
            'sintomatologia': Sintomatologia.objects(paziente_id=patient_id).first(),
            'coinvolgimento_multisistemico': CoinvolgimentoMultisistemico.objects(paziente_id=patient_id).first(),
            'terapia_farmacologica': TerapiaFarmacologica.objects(paziente_id=patient_id).first()
        }
        
        # Only raise NotFound if ALL records are missing
        if all(v is None for v in records.values()):
            raise NotFound(f"No records found for patient {patient_id}")
            
        return records

    def get(self, request, paziente_id):
        """Get complete anamnesis record with available sections"""
        try:
            patient_id = self.validate_paziente_id(paziente_id)
            records = self._get_all_records(patient_id)

            # Find the first available record for common fields
            first_record = next((r for r in records.values() if r is not None), None)
            if not first_record:
                return Response({"message": "No records available"}, status=status.HTTP_404_NOT_FOUND)

            # Prepare base data
            data = {
                'paziente_id': patient_id,
                'operatore_id': first_record.operatore_id,
                'datamanager_id': first_record.datamanager_id,
                'created_at': first_record.created_at,
                'updated_at': max((r.updated_at for r in records.values() if r is not None), default=first_record.updated_at)
            }

            # Add available sections to response with their serializers
            serializer_mapping = {
                'fattori_rischio': FattoriRischioSer,
                'comorbidita': ComorbiditaSer,
                'sintomatologia': SintomatologiaSer,
                'coinvolgimento_multisistemico': CoinvolgimentoMultisistemicoSer,
                'terapia_farmacologica': TerapiaFarmacologicaSer
            }

            for section_name, record in records.items():
                if record is not None:
                    serializer_class = serializer_mapping[section_name]
                    data[section_name] = serializer_class(record).data
                else:
                    data[section_name] = None

            # Add information about missing sections
            missing_sections = [k for k, v in records.items() if v is None]

            # Use the serializer for validation but allow partial data
            serializer = AnamnesiCompletaSer(data=data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            response_data = {
                "message": "Partial data available" if missing_sections else "Complete data available",
                "data": serializer.data
            }

            # Only include missing_sections in response if there are any
            if missing_sections:
                response_data["missing_sections"] = missing_sections

            return Response(response_data)

        except ValidationError as e:
            logger.error(f"Validation error in AnamnesiCompleta GET: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            logger.error(f"Not found error in AnamnesiCompleta GET: {str(e)}")
            return Response({
                "error": str(e),
                "message": "No records found for this patient"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in AnamnesiCompleta GET: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )