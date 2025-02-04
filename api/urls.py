from django.urls import path, register_converter
from rest_framework import routers
from api.views.ecg import ECGViewSet
from api.views.ecocardiogramma import EcocardiogrammaViewSet
from api.views.esami_laboratorio import EsamiLaboratorioViewSet
from api.views.genetica import GeneticaViewSet
from api.views.pedigree import PedigreeViewSet
from api.views.anamnesi import *
from api.views.report import ReportView, QuickReportView

# Custom path converter for positive integers
class PositiveIntConverter:
    regex = r'[1-9][0-9]*'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)

# Register the custom converter
register_converter(PositiveIntConverter, 'pos_int')

router = routers.SimpleRouter()

# Individual anamnesi endpoints
router.register(r'anamnesi/fattori-rischio', FattoriRischioViewSet, basename = "fattori-rischio")
router.register(r'anamnesi/comorbidita', ComorbiditaViewSet, basename = "comorbidita")
router.register(r'anamnesi/sintomatologia', SintomatologiaViewSet, basename = "sintomatologia")
router.register(r'anamnesi/coinvolgimento', CoinvolgimentoViewSet, basename = "coinvolgimento")
router.register(r'anamnesi/terapia', TerapiaViewSet, basename = "terapia")

# Referti Endpoints
router.register(r'ecg', ECGViewSet, basename = "ecg")
router.register(r'pedigree', PedigreeViewSet, basename = "pedigree")
router.register(r'genetica', GeneticaViewSet, basename = "genetica")
router.register(r'ecocardiogramma', EcocardiogrammaViewSet, basename = "ecocardiogramma")
router.register(r'laboratorio', EsamiLaboratorioViewSet, basename = "laboratorio")

urlpatterns = [
    # Individual anamnesi section endpoints
    *router.urls,
    
    # Combined anamnesi endpoint
    path(
        f'anamnesi/<pos_int:paziente_id>/',
        AnamnesiCompletaView.as_view(),
        name='anamnesi-completa'
    ),
    
    # Report endpoints
    path('report/<pos_int:paziente_id>/', ReportView.as_view(), name='report-list'),
    path('report/<pos_int:paziente_id>/<pos_int:report_id>/', ReportView.as_view(), name='report-detail'),
    
    # Quick report endpoints
    path('quickreport/<pos_int:paziente_id>/', QuickReportView.as_view(), name='quick-report-list'),
    path('quickreport/all/', QuickReportAllView.as_view(), name='quick-report-all'),
]