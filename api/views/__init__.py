# api/views/__init__.py
from .anamnesi import (
    FattoriRischioViewSet,
    ComorbiditaViewSet,
    SintomatologiaViewSet,
    CoinvolgimentoViewSet,
    TerapiaViewSet,
    AnamnesiCompletaView,
)

__all__ = [
    'FattoriRischioViewSet',
    'ComorbiditaViewSet',
    'SintomatologiaViewSet',
    'CoinvolgimentoViewSet',
    'TerapiaViewSet',
    'AnamnesiCompletaView',
]