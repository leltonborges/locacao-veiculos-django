from rest_framework import serializers
from .models import Marca, Veiculo, Cliente, Setor, Frota, Alocacao

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class VeiculoSerializer(serializers.ModelSerializer):
    marca_nome = serializers.CharField(source='marca.nome', read_only=True)
    
    class Meta:
        model = Veiculo
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = '__all__'

class FrotaSerializer(serializers.ModelSerializer):
    veiculo_info = serializers.CharField(source='veiculo.__str__', read_only=True)
    
    class Meta:
        model = Frota
        fields = '__all__'

class AlocacaoSerializer(serializers.ModelSerializer):
    unidade_frota_info = serializers.CharField(source='unidade_frota.__str__', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    setor_nome = serializers.CharField(source='setor.nome', read_only=True)
    
    class Meta:
        model = Alocacao
        fields = '__all__' 