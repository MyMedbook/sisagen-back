# api/urls.py
from django.urls import path
from api.views import (
    FattoriRischioView,
    ComorbiditaView,
    SintomatologiaView,
    CoinvolgimentoMultisistemicoView,
    TerapiaFarmacologicaView,
    AnamnesiCompletaView
)

urlpatterns = [
    # Individual section endpoints
    path('anamnesi/fattori-rischio/<str:paziente_id>/', 
         FattoriRischioView.as_view(), 
         name='fattori-rischio'),
         
    path('anamnesi/comorbidita/<str:paziente_id>/', 
         ComorbiditaView.as_view(), 
         name='comorbidita'),
         
    path('anamnesi/sintomatologia/<str:paziente_id>/', 
         SintomatologiaView.as_view(), 
         name='sintomatologia'),
         
    path('anamnesi/coinvolgimento-multisistemico/<str:paziente_id>/', 
         CoinvolgimentoMultisistemicoView.as_view(), 
         name='coinvolgimento-multisistemico'),
         
    path('anamnesi/terapia-farmacologica/<str:paziente_id>/', 
         TerapiaFarmacologicaView.as_view(), 
         name='terapia-farmacologica'),
         
    # Combined endpoint
    path('anamnesi/<str:paziente_id>/', 
         AnamnesiCompletaView.as_view(), 
         name='anamnesi-completa'),
]