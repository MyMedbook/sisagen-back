# api/views/ecg.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
import logging

from api.models.ecg import ECG
from api.serializers.ecg import ECGSerializer
from .base import BasePatientView

logger = logging.getLogger(__name__)

class ECGView(BasePatientView):
    """View for handling ECG records"""
    model = ECG
    serializer_class = ECGSerializer