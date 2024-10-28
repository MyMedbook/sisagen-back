# api/views/__init__.py
from .anamnesi import (
    FattoriRischioView,
    ComorbiditaView,
    SintomatologiaView,
    CoinvolgimentoMultisistemicoView,
    TerapiaFarmacologicaView,
    AnamnesiCompletaView,
)

__all__ = [
    'FattoriRischioView',
    'ComorbiditaView',
    'SintomatologiaView',
    'CoinvolgimentoMultisistemicoView',
    'TerapiaFarmacologicaView',
    'AnamnesiCompletaView',
]