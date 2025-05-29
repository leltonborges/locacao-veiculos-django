from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from .models import Marca, Veiculo, Cliente, Setor, Frota, Alocacao


class MarcaModelTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(
            nome="Toyota",
            pais_origem="Japão",
            fundacao=date(1937, 8, 28),
            website="https://www.toyota.com",
            ativa=True
        )

    def test_marca_creation(self):
        self.assertEqual(self.marca.nome, "Toyota")
        self.assertEqual(self.marca.pais_origem, "Japão")
        self.assertTrue(self.marca.ativa)

    def test_marca_idade(self):
        expected_age = date.today().year - 1937
        self.assertEqual(self.marca.idade, expected_age)

    def test_marca_str(self):
        self.assertEqual(str(self.marca), "Toyota")


class VeiculoModelTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(
            nome="Toyota",
            pais_origem="Japão",
            fundacao=date(1937, 8, 28),
            website="https://www.toyota.com"
        )
        self.veiculo = Veiculo.objects.create(
            modelo="Corolla",
            marca=self.marca,
            tipo="CAR",
            ano_fabricacao=2020
        )

    def test_veiculo_creation(self):
        self.assertEqual(self.veiculo.modelo, "Corolla")
        self.assertEqual(self.veiculo.marca, self.marca)
        self.assertEqual(self.veiculo.tipo, "CAR")
        self.assertEqual(self.veiculo.ano_fabricacao, 2020)

    def test_veiculo_str(self):
        self.assertEqual(str(self.veiculo), "Toyota Corolla")


class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="João Silva",
            cnh="12345678900",
            validade_cnh=date.today() + timedelta(days=365),
            telefone="(11) 99999-9999",
            email="joao@email.com"
        )

    def test_cliente_creation(self):
        self.assertEqual(self.cliente.nome, "João Silva")
        self.assertEqual(self.cliente.cnh, "12345678900")
        self.assertEqual(self.cliente.email, "joao@email.com")

    def test_cnh_valida(self):
        self.assertTrue(self.cliente.cnh_valida)

    def test_cnh_invalida(self):
        self.cliente.validade_cnh = date.today() - timedelta(days=1)
        self.assertFalse(self.cliente.cnh_valida)


class SetorModelTest(TestCase):
    def setUp(self):
        self.setor = Setor.objects.create(
            nome="Departamento de Vendas",
            sigla="DV",
            responsavel="Maria Santos",
            telefone="(11) 3333-3333",
            email="vendas@empresa.com"
        )

    def test_setor_creation(self):
        self.assertEqual(self.setor.nome, "Departamento de Vendas")
        self.assertEqual(self.setor.sigla, "DV")
        self.assertEqual(self.setor.responsavel, "Maria Santos")

    def test_setor_str(self):
        self.assertEqual(str(self.setor), "Departamento de Vendas (DV)")


class FrotaModelTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(
            nome="Toyota",
            pais_origem="Japão",
            fundacao=date(1937, 8, 28),
            website="https://www.toyota.com"
        )
        self.veiculo = Veiculo.objects.create(
            modelo="Corolla",
            marca=self.marca,
            tipo="CAR",
            ano_fabricacao=2020
        )
        self.frota = Frota.objects.create(
            veiculo=self.veiculo,
            placa="ABC1234",
            km_atual=10000,
            disponivel=True
        )

    def test_frota_creation(self):
        self.assertEqual(self.frota.veiculo, self.veiculo)
        self.assertEqual(self.frota.placa, "ABC1234")
        self.assertEqual(self.frota.km_atual, 10000)
        self.assertTrue(self.frota.disponivel)

    def test_frota_str(self):
        self.assertEqual(str(self.frota), "Toyota Corolla - ABC1234")

    def test_unidades_disponiveis(self):
        self.assertEqual(Frota.unidades_disponiveis().count(), 1)
        self.assertEqual(Frota.unidades_disponiveis(self.veiculo.id).count(), 1)


class AlocacaoModelTest(TestCase):
    def setUp(self):
        # Criar Marca
        self.marca = Marca.objects.create(
            nome="Toyota",
            pais_origem="Japão",
            fundacao=date(1937, 8, 28),
            website="https://www.toyota.com"
        )
        
        # Criar Veículo
        self.veiculo = Veiculo.objects.create(
            modelo="Corolla",
            marca=self.marca,
            tipo="CAR",
            ano_fabricacao=2020
        )
        
        # Criar Frota
        self.frota = Frota.objects.create(
            veiculo=self.veiculo,
            placa="ABC1234",
            km_atual=10000,
            disponivel=True
        )
        
        # Criar Cliente
        self.cliente = Cliente.objects.create(
            nome="João Silva",
            cnh="12345678900",
            validade_cnh=date.today() + timedelta(days=365),
            telefone="(11) 99999-9999",
            email="joao@email.com"
        )
        
        # Criar Setor
        self.setor = Setor.objects.create(
            nome="Departamento de Vendas",
            sigla="DV",
            responsavel="Maria Santos",
            telefone="(11) 3333-3333",
            email="vendas@empresa.com"
        )
        
        # Criar Alocação
        self.alocacao = Alocacao.objects.create(
            unidade_frota=self.frota,
            cliente=self.cliente,
            setor=self.setor,
            data_alocacao=timezone.now(),
            km_inicial=10000,
            motivo="Viagem de negócios"
        )

    def test_alocacao_creation(self):
        self.assertEqual(self.alocacao.unidade_frota, self.frota)
        self.assertEqual(self.alocacao.cliente, self.cliente)
        self.assertEqual(self.alocacao.setor, self.setor)
        self.assertEqual(self.alocacao.km_inicial, 10000)
        self.assertIsNone(self.alocacao.data_devolucao)

    def test_alocacao_em_uso(self):
        self.assertTrue(self.alocacao.em_uso)

    def test_alocacao_devolucao(self):
        self.alocacao.data_devolucao = timezone.now()
        self.alocacao.km_final = 10500
        self.alocacao.save()
        
        self.assertFalse(self.alocacao.em_uso)
        self.assertEqual(self.alocacao.km_percorridos, 500)
        self.assertTrue(self.frota.disponivel)
        self.assertEqual(self.frota.km_atual, 10500)
