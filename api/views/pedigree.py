# api/views/pedigree.py
import logging
from api.models.pedigree import Pedigree
from api.serializers.pedigree import PedigreeSerializer
from api.views.base import SisagenViewSet

logger = logging.getLogger(__name__)

class PedigreeViewSet(SisagenViewSet):

    model = Pedigree
    serializer_class = PedigreeSerializer