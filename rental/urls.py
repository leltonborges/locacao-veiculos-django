from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('alocar/', views.alocar_veiculo, name='alocar_veiculo'),
    path('alocar/<int:veiculo_id>/', views.alocar_veiculo_detalhes, name='alocar_veiculo_detalhes'),
]