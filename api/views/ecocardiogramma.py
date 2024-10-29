from rest_framework.exceptions import NotFound, ValidationError
import logging
from api.models.ecocardiogramma import Ecocardiogramma
from api.serializers.ecocardiogramma import EcocardiogrammaSerializer
from .base import BasePatientView

logger = logging.getLogger(__name__)

class EcocardiogrammaView(BasePatientView):
    """View for handling echocardiogram results"""
    model = Ecocardiogramma
    serializer_class = EcocardiogrammaSerializer