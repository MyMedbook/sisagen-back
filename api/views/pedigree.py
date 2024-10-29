# api/views/pedigree.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
import logging

from api.models.pedigree import (
    Pedigree, DirectFamilyMember, NumberedFamilyMember
)
from api.serializers.pedigree import PedigreeSerializer

logger = logging.getLogger(__name__)

class PedigreeView(APIView):
    def _create_family_member(self, data, numbered=False):
        """Helper method to create family member instances"""
        if data is None:
            return None
            
        if numbered:
            return NumberedFamilyMember(**data)
        return DirectFamilyMember(**data)
    def get(self, request, paziente_id):
        """Get pedigree record for a specific patient"""
        try:
            # Validate patient ID
            try:
                pid = int(paziente_id)
                if pid <= 0:
                    raise ValidationError("paziente_id must be positive")
            except ValueError:
                raise ValidationError("paziente_id must be a valid integer")

            # Get instance
            instance = Pedigree.objects(paziente_id=pid).first()
            if not instance:
                raise NotFound(f"Pedigree not found for patient {paziente_id}")

            # Serialize and return
            serializer = PedigreeSerializer(instance)
            return Response(serializer.data)

        except ValidationError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except NotFound as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error in Pedigree GET: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def put(self, request, paziente_id):
        """Create or update pedigree record"""
        try:
            # Validate patient ID
            try:
                pid = int(paziente_id)
                if pid <= 0:
                    raise ValidationError("paziente_id must be positive")
            except ValueError:
                raise ValidationError("paziente_id must be a valid integer")

            # Get existing instance if any
            instance = Pedigree.objects(paziente_id=pid).first()
            
            # Validate data with serializer
            serializer = PedigreeSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            
            # Create or update the instance
            if instance:
                # Update direct family members
                for field in ['padre', 'madre', 'nonno_paterno', 'nonna_paterna', 
                            'nonno_materno', 'nonna_materna']:
                    if field in validated_data:
                        setattr(instance, field, 
                               self._create_family_member(validated_data.get(field)))
                
                # Update numbered family members
                if 'fratelli' in validated_data:
                    instance.fratelli = [
                        self._create_family_member(member, numbered=True)
                        for member in validated_data['fratelli']
                    ]
                
                if 'figli' in validated_data:
                    instance.figli = [
                        self._create_family_member(member, numbered=True)
                        for member in validated_data['figli']
                    ]
                
                instance.save()
            else:
                # Create new instance
                new_data = validated_data.copy()
                
                # Handle direct family members
                for field in ['padre', 'madre', 'nonno_paterno', 'nonna_paterna', 
                            'nonno_materno', 'nonna_materna']:
                    if field in new_data:
                        new_data[field] = self._create_family_member(new_data[field])
                
                # Handle numbered family members
                if 'fratelli' in new_data:
                    new_data['fratelli'] = [
                        self._create_family_member(member, numbered=True)
                        for member in new_data['fratelli']
                    ]
                
                if 'figli' in new_data:
                    new_data['figli'] = [
                        self._create_family_member(member, numbered=True)
                        for member in new_data['figli']
                    ]
                
                instance = Pedigree(**new_data)
                instance.save()
            
            return Response(
                PedigreeSerializer(instance).data,
                status=status.HTTP_200_OK if instance else status.HTTP_201_CREATED
            )
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in Pedigree PUT: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def delete(self, request, paziente_id):
        """Delete pedigree record for a specific patient"""
        try:
            # Validate patient ID
            try:
                pid = int(paziente_id)
                if pid <= 0:
                    raise ValidationError("paziente_id must be positive")
            except ValueError:
                raise ValidationError("paziente_id must be a valid integer")

            # Get instance
            instance = Pedigree.objects(paziente_id=pid).first()
            if not instance:
                raise NotFound(f"Pedigree not found for patient {paziente_id}")

            # Delete the instance
            instance.delete()

            return Response(
                {"message": f"Pedigree for patient {paziente_id} deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except ValidationError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except NotFound as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error in Pedigree DELETE: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )