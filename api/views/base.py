# api/views/base.py
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError, ParseError
from mongoengine.queryset.visitor import Q
from authentication.permissions import SisagenPermission
from api.models.base import BaseDocument
from api.serializers.base import BaseSerializer
from datetime import datetime
from json import loads
import logging

logger = logging.getLogger(__name__)

def to_json(query):
    return loads(query.to_json())


class SisagenViewSet(ViewSet):

    permission_classes = [SisagenPermission]
    model: BaseDocument = None
    serializer_class: BaseSerializer = None

    def get_mongoquery(self):

        return self.model.objects().order_by('-created_at')
    
    def query_param_int(self, keyword, default=None):

        param = self.request.query_params.get(keyword, default)

        if not param:
            return None
        
        try:
            int_param = int(param)
            if int_param < 0:
                raise ParseError(f"{keyword} query_param must not be negative (given value: {int_param})")
            else:
                return int_param
        except (ValueError, TypeError) as e:
            raise ParseError(f"{keyword} query_param must be a positive integer (given value: {param})")
    
    def paginate(self, instances):

        page_number = self.query_param_int("page", 1)
        items_per_page = self.query_param_int("pagesize", 10)
  
        offset = (page_number - 1)*items_per_page

        return instances.skip(offset).limit(items_per_page)

    def list(self, request):

        instances = self.get_mongoquery()

        if (paziente_id := request.query_params.get('paziente_id')):
            instances = instances(paziente_id=paziente_id)

        if (operatore_id := request.query_params.get('operatore_id')):
            instances = instances(operatore_id=operatore_id)

        if (datamanager_id := request.query_params.get('datamanager_id')):
            is_datamanager = Q(datamanager_id=datamanager_id)
            operator_entered = Q(datamanager_id__exists=False) & Q(operatore_id=datamanager_id)
            instances = instances(is_datamanager | operator_entered)
        
        if not (count := instances.count()):
            raise NotFound(f"No documents of type {self.model.__name__} found matching query criteria.")

        if request.query_params.get("page"):
            instances = self.paginate(instances)
            return Response(dict(
                count=count, 
                results=to_json(instances)
                ))

        return Response(to_json(instances))
    
    def create(self, request):

        data = request.data.copy()
        serializer = self.serializer_class(data=data, context={'request': request})
        if not serializer.is_valid():
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        instance = self.model(**serializer.data)
        try:
            instance.validate()
        except ValidationError as e:
            Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        instance.save()
    
        return Response(
            to_json(instance),
            status.HTTP_201_CREATED
            )
    
    def retrieve(self, request, pk):
        
        instances = self.get_mongoquery()
        instances = instances = instances(paziente_id=pk)
        if not (count := instances.count()):
            raise NotFound(f"No documents of type {self.model.__name__} found for patient with id {pk}.")
        
        if request.query_params.get("page"):
            instances = self.paginate(instances)
            return Response(dict(
                count=count, 
                results=to_json(instances)
                ))

        return Response(to_json(instances))
    
    @action(detail=True)
    def latest(self, request, pk):
        
        instances = self.get_mongoquery()
        instances = instances = instances(paziente_id=pk)

        if not instances.count():
            raise NotFound(f"No documents of type {self.model.__name__} found for patient with id {pk}.")

        return Response(to_json(instances.first()))


class BaseSisagenView(APIView):
    """Base view for handling patient-related records"""
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


class BasePatientView(BaseSisagenView):

    def get(self, request, paziente_id):
        """Get record"""
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
        """Create or update record"""
        try:
            pid = self.validate_paziente_id(paziente_id)
            instance = self.get_object(pid)
            
            # Prepare data
            data = request.data.copy()
            data['paziente_id'] = pid
            
            if instance:
                # Update existing record
                serializer = self.serializer_class(instance, data=data)
            else:
                # Create new record
                serializer = self.serializer_class(data=data)
                
            if not serializer.is_valid():
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create or update instance
            if instance:
                for key, value in serializer.validated_data.items():
                    setattr(instance, key, value)
                instance.save()
            else:
                instance = self.model(**serializer.validated_data)
                instance.save()
            
            return Response(
                self.serializer_class(instance).data,
                status=status.HTTP_200_OK if instance else status.HTTP_201_CREATED
            )
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in PUT: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )