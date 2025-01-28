from django.urls import path, register_converter
from api.views import (
    FattoriRischioView, ComorbiditaView, SintomatologiaView,
    CoinvolgimentoMultisistemicoView, TerapiaFarmacologicaView,
    AnamnesiCompletaView
)
from api.views.ecg import ECGView
from api.views.ecocardiogramma import EcocardiogrammaView
from api.views.esami_laboratorio import EsamiLaboratorioView
from api.views.genetica import GeneticaView
from api.views.pedigree import PedigreeView
from api.views.anamnesi_nu import *
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

# URL patterns grouped by feature
class AnamnesiURLs:
    BASE = 'anamnesi_old'
    SECTIONS = {
        'fattori-rischio': FattoriRischioView,
        'comorbidita': ComorbiditaView,
        'sintomatologia': SintomatologiaView,
        'coinvolgimento-multisistemico': CoinvolgimentoMultisistemicoView,
        'terapia-farmacologica': TerapiaFarmacologicaView,
    }

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'anamnesi/fattori-rischio', FattoriRischioViewSet, basename = "fattori-rischio")
router.register(r'anamnesi/comorbidita', ComorbiditaViewSet, basename = "comorbidita")
router.register(r'anamnesi/sintomatologia', SintomatologiaViewSet, basename = "sintomatologia")
router.register(r'anamnesi/coinvolgimento', CoinvolgimentoViewSet, basename = "coinvolgimento")
router.register(r'anamnesi/terapia', TerapiaViewSet, basename = "terapia")

urlpatterns = router.urls

urlpatterns = [
    # Individual anamnesi section endpoints
    *router.urls,
    *[
        path(
            f'{AnamnesiURLs.BASE}/{section}/<pos_int:paziente_id>/',
            view.as_view(),
            name=f'{section}-list'
        )
        for section, view in AnamnesiURLs.SECTIONS.items()
    ],
    
    # Combined anamnesi endpoint
    path(
        f'anamnesi/<pos_int:paziente_id>/',
        AnamnesiCompletaNuView.as_view(),
        name='anamnesi-completa'
    ),
    
    # Other endpoints
    path('ecg/<pos_int:paziente_id>/', ECGView.as_view(), name='ecg-list'),
    path('ecocardiogramma/<pos_int:paziente_id>/', EcocardiogrammaView.as_view(), name='ecocardiogramma-list'),
    path('esami-laboratorio/<pos_int:paziente_id>/', EsamiLaboratorioView.as_view(), name='esami-laboratorio-list'),
    path('genetica/<pos_int:paziente_id>/', GeneticaView.as_view(), name='genetica-list'),
    path('pedigree/<pos_int:paziente_id>/', PedigreeView.as_view(), name='pedigree-list'),
    
    # Report endpoints
    path('report/<pos_int:paziente_id>/', ReportView.as_view(), name='report-list'),
    path('report/<pos_int:paziente_id>/<pos_int:report_id>/', ReportView.as_view(), name='report-detail'),
    
    # Quick report endpoint
    path('quickreport/<pos_int:paziente_id>/', QuickReportView.as_view(), name='quick-report-list'),
]