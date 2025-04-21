from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('alocar/', views.criar_alocacao, name='alocar_veiculo'),
    path('veiculos/<int:veiculo_id>/frota-disponivel/', views.frota_disponivel_por_veiculo,
         name='frota_disponivel_por_veiculo'),
    path('frota/<int:frota_id>/km/', views.km_frota, name='km_frota'),
]
