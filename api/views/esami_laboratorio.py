# api/views/esami_laboratorio.py
from rest_framework.exceptions import NotFound, ValidationError
import logging
from api.models.esami_laboratorio import EsamiLaboratorio
from api.serializers.esami_laboratorio import EsamiLaboratorioSerializer
from .base import BasePatientView

logger = logging.getLogger(__name__)

class EsamiLaboratorioView(BasePatientView):
    """View for handling laboratory test results"""
    model = EsamiLaboratorio
    serializer_class = EsamiLaboratorioSerializer