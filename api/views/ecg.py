# api/views/ecg.py
import logging
from api.models.ecg import ECG
from api.serializers.ecg import ECGSerializer
from api.views.base import SisagenViewSet

logger = logging.getLogger(__name__)
 
class ECGViewSet(SisagenViewSet):
    """Viewset for handling ECG records"""
    model = ECG
    serializer_class = ECGSerializer