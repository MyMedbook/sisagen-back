# api/urls.py
from django.urls import path, register_converter
from api.views import (
    FattoriRischioView,
    ComorbiditaView,
    SintomatologiaView,
    CoinvolgimentoMultisistemicoView,
    TerapiaFarmacologicaView,
    AnamnesiCompletaView
)
from api.views.ecg import ECGView
from api.views.ecocardiogramma import EcocardiogrammaView
from api.views.esami_laboratorio import EsamiLaboratorioView
from api.views.genetica import GeneticaView
from api.views.pedigree import PedigreeView

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
    BASE = 'anamnesi'
    SECTIONS = {
        'fattori-rischio': FattoriRischioView,
        'comorbidita': ComorbiditaView,
        'sintomatologia': SintomatologiaView,
        'coinvolgimento-multisistemico': CoinvolgimentoMultisistemicoView,
        'terapia-farmacologica': TerapiaFarmacologicaView,
    }

class PedigreeURLs:
    BASE = 'pedigree'
    SECTIONS = {
        '': PedigreeView  # Empty string as key for base endpoint
    }

class GeneticaURLs:
    BASE = 'genetica'
    SECTIONS = {
        '': GeneticaView  # Empty string as key for base endpoint
    }

class ECGURLs:
    BASE = 'ecg'
    SECTIONS = {
        '': ECGView  # Empty string as key for base endpoint
    }

class EsamiLaboratorioURLs:
    BASE = 'esami-laboratorio'
    SECTIONS = {
        '': EsamiLaboratorioView
    }

class EcocardiogrammaURLs:
    BASE = 'ecocardiogramma'
    SECTIONS = {
        '': EcocardiogrammaView
    }


# Generate URL patterns
urlpatterns = [
    # Individual anamnesi section endpoints
    *[
        path(
            f'{AnamnesiURLs.BASE}/{section}/<pos_int:paziente_id>/',
            view.as_view(),
            name=section
        )
        for section, view in AnamnesiURLs.SECTIONS.items()
    ],
    
    # Combined anamnesi endpoint
    path(
        f'{AnamnesiURLs.BASE}/<pos_int:paziente_id>/',
        AnamnesiCompletaView.as_view(),
        name='anamnesi-completa'
    ),
    
    # Pedigree endpoints
    *[
        path(
            f'{PedigreeURLs.BASE}/{section}<pos_int:paziente_id>/',
            view.as_view(),
            name=f'pedigree{"-"+section if section else ""}'
        )
        for section, view in PedigreeURLs.SECTIONS.items()
    ],
    
    # Genetica endpoints
    *[
        path(
            f'{GeneticaURLs.BASE}/{section}<pos_int:paziente_id>/',
            view.as_view(),
            name=f'genetica{"-"+section if section else ""}'
        )
        for section, view in GeneticaURLs.SECTIONS.items()
    ],
    
    # ECG endpoints
    *[
        path(
            f'{ECGURLs.BASE}/{section}<pos_int:paziente_id>/',
            view.as_view(),
            name=f'ecg{"-"+section if section else ""}'
        )
        for section, view in ECGURLs.SECTIONS.items()
    ],
    # Esami Laboratorio endpoints
        *[
        path(
            f'{EsamiLaboratorioURLs.BASE}/{section}<pos_int:paziente_id>/',
            view.as_view(),
            name=f'esami-laboratorio{"-"+section if section else ""}'
        )
        for section, view in EsamiLaboratorioURLs.SECTIONS.items()
    ],
    
    # Ecocardiogramma endpoints
    *[
        path(
            f'{EcocardiogrammaURLs.BASE}/{section}<pos_int:paziente_id>/',
            view.as_view(),
            name=f'ecocardiogramma{"-"+section if section else ""}'
        )
        for section, view in EcocardiogrammaURLs.SECTIONS.items()
    ],

]