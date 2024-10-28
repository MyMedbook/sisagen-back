# api/serializers/__init__.py
from .anamnesi import (
    FattoriRischioSer,
    ComorbiditaSer,
    SintomatologiaSer,
    CoinvolgimentoMultisistemicoSer,
    TerapiaFarmacologicaSer,
    AnamnesiCompletaSer
)

__all__ = [
    'FattoriRischioSer',
    'ComorbiditaSer',
    'SintomatologiaSer',
    'CoinvolgimentoMultisistemicoSer',
    'TerapiaFarmacologicaSer',
    'AnamnesiCompletaSer'
]