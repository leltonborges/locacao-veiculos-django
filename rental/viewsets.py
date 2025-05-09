from rest_framework import viewsets
from .models import Marca, Veiculo, Cliente, Setor, Frota, Alocacao
from .serializers import (
    MarcaSerializer, VeiculoSerializer, ClienteSerializer,
    SetorSerializer, FrotaSerializer, AlocacaoSerializer
)

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer

class FrotaViewSet(viewsets.ModelViewSet):
    queryset = Frota.objects.all()
    serializer_class = FrotaSerializer

class AlocacaoViewSet(viewsets.ModelViewSet):
    queryset = Alocacao.objects.all()
    serializer_class = AlocacaoSerializer 