import logging
from api.models.ecocardiogramma import Ecocardiogramma
from api.serializers.ecocardiogramma import EcocardiogrammaSerializer
from .base import SisagenViewSet

logger = logging.getLogger(__name__)
 
class EcocardiogrammaViewSet(SisagenViewSet):
    """View for handling echocardiogram results"""
    model = Ecocardiogramma
    serializer_class = EcocardiogrammaSerializer