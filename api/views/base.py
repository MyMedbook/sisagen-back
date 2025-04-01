# api/views/base.py
import requests
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError, ParseError
from rest_framework.pagination import PageNumberPagination
from mongoengine.queryset.visitor import Q
from authentication.permissions import SisagenPermission, sisagen_rank
from api.models.base import BaseDocument
from api.serializers.base import BaseSerializer
from api.rendering import PdfMixin
from datetime import datetime
from json import loads
import logging

logger = logging.getLogger(__name__)

def to_json(query):
    return loads(query.to_json())

class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pagesize'
    max_page_size = 100


class SisagenViewSet(ViewSet, PdfMixin):

    permission_classes = [SisagenPermission]
    model: BaseDocument = None
    serializer_class: BaseSerializer = None
    pagination_class = ReportPagination
    pdf_renderer = None

    def get_paginated_response(self, data):
        """Helper method to get paginated response"""
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(data, self.request)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    def get_mongoquery(self):

        rank = sisagen_rank(self.request.user)

        qset = self.model.objects()

        if rank == "Sisagen_Paziente":
            qset = qset(paziente_id=self.request.user.pk)

        if rank == "Sisagen_Specialista":
            qset = qset(operatore_id=self.request.user.pk)

        return qset.order_by('-created_at')
    
    
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
        
        if not instances.count():
            raise NotFound(f"No documents of type {self.model.__name__} found matching query criteria.")
        
        return self.get_paginated_response(instances)

    
    def create(self, request):

        data = request.data.copy()

        query_params = "&".join([f"{param}={data[param]}"
                                 for param in ["paziente_id", "operatore_id", "structure_id"]])
        verification_url = f"https://mymedbook.it/api/v1/sisagen/verification/?{query_params}"

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        headers = {"Authorization": auth_header}

        verify_response = requests.get(
                verification_url,
                headers=headers
            )

        if verify_response.status_code != 200:
            return Response(verify_response.json(), status=verify_response.status_code)
        
        verification = verify_response.json()
        data["structure"] = verification["structure"]
        operator = verification["operator"]
        patient = verification["patient"]
        dossier_id = verification["dossier_id"]

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
        # instance.save()

        nu_serializer = self.serializer_class(instance)
        report = nu_serializer.data

        document_response = self.render_report(operator, patient, report, dossier_id)
        
        return Response(
            dict(**nu_serializer.data, document=document_response.json()),
            status.HTTP_201_CREATED
            )
    
    def retrieve(self, request, pk):
        
        instances = self.get_mongoquery()
        instances = instances(paziente_id=pk)
        if not (count := instances.count()):
            raise NotFound(f"No documents of type {self.model.__name__} found for patient with id {pk}.")
        
        return self.get_paginated_response(instances)

    
    @action(detail=True)
    def latest(self, request, pk):
        
        instances = self.get_mongoquery()
        instances = instances(paziente_id=pk)

        if not instances.count():
            raise NotFound(f"No documents of type {self.model.__name__} found for patient with id {pk}.")
        
        serializer = self.serializer_class(instances.first())

        return Response(serializer.data)


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