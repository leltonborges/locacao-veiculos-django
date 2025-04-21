from django.urls import path

from rental.views.clientes.views import listar_clientes, criar_cliente, detalhar_cliente, editar_cliente, \
    deletar_cliente
from rental.views.core.views import home
from rental.views.alocacoes.views import criar_alocacao, listar_alocacoes, detalhar_alocacao
from rental.views.alocacoes.api import frota_disponivel_por_veiculo, km_frota
from rental.views.frota.views import listar_frota, criar_frota, detalhar_frota, editar_frota, deletar_frota
from rental.views.marcas.views import listar_marcas, criar_marca, detalhar_marca, editar_marca, deletar_marca
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
    path('marcas/', listar_marcas, name='listar_marcas'),
    path('marcas/new/', criar_marca, name='criar_marca'),
    path('marcas/<int:marca_id>/', detalhar_marca, name='detalhar_marca'),
    path('marcas/<int:marca_id>/edit/', editar_marca, name='editar_marca'),
    path('marcas/<int:marca_id>/delete/', deletar_marca, name='deletar_marca'),
    path('clientes/', listar_clientes, name='listar_clientes'),
    path('clientes/new/', criar_cliente, name='criar_cliente'),
    path('clientes/<int:cliente_id>/', detalhar_cliente, name='detalhar_cliente'),
    path('clientes/<int:cliente_id>/edit/', editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/delete/', deletar_cliente, name='deletar_cliente'),
]
