# api/views/genetica.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
import logging

from api.models.genetica import Genetica
from api.serializers.genetica import GeneticaSerializer
from .base import BasePatientView

logger = logging.getLogger(__name__)

class GeneticaView(BasePatientView):
    """View for handling genetic information"""
    model = Genetica
    serializer_class = GeneticaSerializer