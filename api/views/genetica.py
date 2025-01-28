# api/views/genetica.py
import logging

from api.models.genetica import Genetica
from api.serializers.genetica import GeneticaSerializer
from .base import SisagenViewSet

logger = logging.getLogger(__name__)

class GeneticaViewSet(SisagenViewSet):
    """View for handling genetic information"""
    model = Genetica
    serializer_class = GeneticaSerializer