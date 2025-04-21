from django.urls import path
from rental.views.core.views import home
from rental.views.alocacoes.views import criar_alocacao
from rental.views.alocacoes.api import frota_disponivel_por_veiculo, km_frota

urlpatterns = [
    path('', home, name='home'),
    path('alocar/', criar_alocacao, name='alocar_veiculo'),

    # APIs
    path('api/veiculos/<int:veiculo_id>/frota-disponivel/', frota_disponivel_por_veiculo,
         name='frota_disponivel_por_veiculo'),
    path('api/frota/<int:frota_id>/km/', km_frota, name='km_frota'),
]