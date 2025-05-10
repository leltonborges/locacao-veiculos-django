from rest_framework import viewsets
from .models import Marca, Veiculo, Cliente, Setor, Frota, Alocacao
from .serializers import (
    MarcaSerializer, VeiculoSerializer, ClienteSerializer,
    SetorSerializer, FrotaSerializer, AlocacaoSerializer
)

class MarcaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar marcas de veículos.
    
    Permite listar, criar, atualizar e excluir marcas.
    """
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class VeiculoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar modelos de veículos.
    
    Permite listar, criar, atualizar e excluir veículos.
    Inclui informações sobre a marca associada.
    """
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar clientes.
    
    Permite listar, criar, atualizar e excluir clientes.
    Inclui informações de CNH e contato.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class SetorViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar setores.
    
    Permite listar, criar, atualizar e excluir setores.
    Inclui informações sobre responsáveis e contatos.
    """
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer

class FrotaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar unidades da frota.
    
    Permite listar, criar, atualizar e excluir unidades.
    Inclui informações sobre o veículo e sua disponibilidade.
    """
    queryset = Frota.objects.all()
    serializer_class = FrotaSerializer

class AlocacaoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar alocações de veículos.
    
    Permite listar, criar, atualizar e excluir alocações.
    Inclui informações sobre cliente, setor e período de alocação.
    """
    queryset = Alocacao.objects.all()
    serializer_class = AlocacaoSerializer 