# api/views/anamnesi.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from datetime import datetime
from bson import ObjectId

from api.models import (
    FattoriRischio, Comorbidita, Sintomatologia,
    CoinvolgimentoMultisistemico, TerapiaFarmacologica
)
from api.serializers import (
    FattoriRischioSer, ComorbiditaSer, SintomatologiaSer,
    CoinvolgimentoMultisistemicoSer, TerapiaFarmacologicaSer,
    AnamnesiCompletaSer
)

class BaseAnamnesisView(APIView):
    model = None
    serializer_class = None

    def get_object(self, paziente_id):
        try:
            return self.model.objects.get(paziente_id=ObjectId(paziente_id))
        except self.model.DoesNotExist:
            raise NotFound(f"{self.model.__name__} not found")

    def get(self, request, paziente_id):
        instance = self.get_object(paziente_id)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def post(self, request, paziente_id):
        request.data['paziente_id'] = paziente_id
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            # Convert string IDs to ObjectId
            data = serializer.validated_data
            data['paziente_id'] = ObjectId(paziente_id)
            data['operatore_id'] = ObjectId(data['operatore_id'])
            
            instance = self.model(**data)
            instance.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, paziente_id):
        instance = self.get_object(paziente_id)
        request.data['paziente_id'] = paziente_id
        serializer = self.serializer_class(instance, data=request.data)
        
        if serializer.is_valid():
            # Convert string IDs to ObjectId
            data = serializer.validated_data
            data['paziente_id'] = ObjectId(paziente_id)
            data['operatore_id'] = ObjectId(data['operatore_id'])
            data['updated_at'] = datetime.utcnow()
            
            for key, value in data.items():
                setattr(instance, key, value)
            instance.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, paziente_id):
        instance = self.get_object(paziente_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    def get(self, request, paziente_id):
        try:
            # Convert string ID to ObjectId
            patient_obj_id = ObjectId(paziente_id)
            
            # Fetch all anamnesis data for the patient
            fattori_rischio = FattoriRischio.objects.get(paziente_id=patient_obj_id)
            comorbidita = Comorbidita.objects.get(paziente_id=patient_obj_id)
            sintomatologia = Sintomatologia.objects.get(paziente_id=patient_obj_id)
            coinvolgimento = CoinvolgimentoMultisistemico.objects.get(paziente_id=patient_obj_id)
            terapia = TerapiaFarmacologica.objects.get(paziente_id=patient_obj_id)

            # Combine all data
            data = {
                'paziente_id': str(patient_obj_id),
                'operatore_id': str(fattori_rischio.operatore_id),  # Using the most recent operator
                'created_at': fattori_rischio.created_at,
                'updated_at': max(
                    x.updated_at for x in [
                        fattori_rischio, comorbidita, sintomatologia,
                        coinvolgimento, terapia
                    ]
                ),
                'fattori_rischio': FattoriRischioSer(fattori_rischio).data,
                'comorbidita': ComorbiditaSer(comorbidita).data,
                'sintomatologia': SintomatologiaSer(sintomatologia).data,
                'coinvolgimento_multisistemico': CoinvolgimentoMultisistemicoSer(coinvolgimento).data,
                'terapia_farmacologica': TerapiaFarmacologicaSer(terapia).data
            }

            serializer = AnamnesiCompletaSer(data=data)
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (FattoriRischio.DoesNotExist, Comorbidita.DoesNotExist,
                Sintomatologia.DoesNotExist, CoinvolgimentoMultisistemico.DoesNotExist,
                TerapiaFarmacologica.DoesNotExist) as e:
            raise NotFound("Anamnesi data incomplete")
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )