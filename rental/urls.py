from django.urls import path
from rental.views.core.views import home
from rental.views.alocacoes.views import criar_alocacao, listar_alocacoes, detalhar_alocacao
from rental.views.alocacoes.api import frota_disponivel_por_veiculo, km_frota
from rental.views.frota.views import listar_frota, criar_frota, detalhar_frota, editar_frota, deletar_frota
from rental.views.veiculos.views import listar_veiculos, criar_veiculo, editar_veiculo, detalhar_veiculo

urlpatterns = [
    path('', home, name='home'),
    path('alocar/', listar_alocacoes, name='listar_alocacoes'),
    path('alocar/new/', criar_alocacao, name='criar_alocacao'),
    path('alocar/<int:alocacao_id>/', detalhar_alocacao, name='detalhar_alocacao'),
    path('api/veiculos/<int:veiculo_id>/frota-disponivel/', frota_disponivel_por_veiculo,
         name='frota_disponivel_por_veiculo'),
    path('api/frota/<int:frota_id>/km/', km_frota, name='km_frota'),
    path('veiculos/', listar_veiculos, name='listar_veiculos'),
    path('veiculos/new/', criar_veiculo, name='criar_veiculo'),
    path('veiculos/<int:veiculo_id>/', detalhar_veiculo, name='detalhar_veiculo'),
    path('veiculos/<int:veiculo_id>/edit/', editar_veiculo, name='editar_veiculo'),
    path('frota/', listar_frota, name='listar_frota'),
    path('frota/new/', criar_frota, name='criar_frota'),
    path('frota/<int:frota_id>/', detalhar_frota, name='detalhar_frota'),
    path('frota/<int:frota_id>/edit/', editar_frota, name='editar_frota'),
    path('frota/<int:frota_id>/delete/', deletar_frota, name='deletar_frota'),
]
