# api/views/esami_laboratorio.py
import logging
from api.models.esami_laboratorio import EsamiLaboratorio
from api.serializers.esami_laboratorio import EsamiLaboratorioSerializer
from .base import SisagenViewSet

logger = logging.getLogger(__name__)

class EsamiLaboratorioViewSet(SisagenViewSet):
    """View for handling laboratory test results"""
    model = EsamiLaboratorio
    serializer_class = EsamiLaboratorioSerializer