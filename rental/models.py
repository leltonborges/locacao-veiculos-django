from django.db import models
from django.db.models import Count, Q
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Marca(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome da Marca")
    pais_origem = models.CharField(max_length=50, verbose_name="País de Origem")
    fundacao = models.DateField(verbose_name="Ano de Fundação")
    website = models.URLField(verbose_name="Site Oficial")
    ativa = models.BooleanField(default=True, verbose_name="Marca Ativa?")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['nome']

    @property
    def idade(self):
        from datetime import date
        return date.today().year - self.fundacao.year

    @property
    def veiculos_count(self):
        return self.veiculos.count()

    def __str__(self):
        return self.nome


class VeiculoQuerySet(models.QuerySet):
    def annotate_disponiveis(self):
        return self.annotate(
            unidades_disponiveis=Count(
                'unidades_frota',
                filter=Q(unidades_frota__disponivel=True)
            )
        )


class Veiculo(models.Model):
    TIPO_CHOICES = [
        ('CAR', 'Carro'),
        ('MOT', 'Motocicleta'),
        ('CAM', 'Caminhão'),
        ('VAN', 'Van'),
    ]
    objects = VeiculoQuerySet.as_manager()

    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    marca = models.ForeignKey(
        'Marca',
        on_delete=models.PROTECT,
        related_name='veiculos',
        verbose_name="Marca"
    )
    tipo = models.CharField(
        max_length=3,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Veículo"
    )
    ano_fabricacao = models.PositiveIntegerField(verbose_name="Ano de Fabricação")

    class Meta:
        verbose_name = "Modelo de Veículo"
        verbose_name_plural = "Modelos de Veículos"
        ordering = ['marca', 'modelo']

    def __str__(self):
        return f"{self.marca} {self.modelo}"


class Cliente(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    cnh = models.CharField(max_length=20, unique=True, verbose_name="Número da CNH")
    validade_cnh = models.DateField(verbose_name="Validade da CNH")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(unique=True, verbose_name="E-mail")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    @property
    def cnh_valida(self):
        from datetime import date
        if self.validade_cnh is None:
            return False
        return date.today() <= self.validade_cnh

    @property
    def alocacoes_count(self):
        return self.alocacoes.count()

    def __str__(self):
        return self.nome


class Setor(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Setor")
    sigla = models.CharField(max_length=10, unique=True, verbose_name="Sigla")
    responsavel = models.CharField(max_length=100, verbose_name="Responsável")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail do Setor")

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        ordering = ['nome']

    @property
    def alocacoes_count(self):
        return self.alocacoes.count()

    @property
    def veiculos_alocados(self):
        return ", ".join([str(a.veiculo) for a in self.alocacoes.filter(data_devolucao__isnull=True)])

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Frota(models.Model):
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name='unidades_frota'
    )
    placa = models.CharField(max_length=10, unique=True, verbose_name="Placa")
    km_atual = models.PositiveIntegerField(default=0, verbose_name="Quilometragem Atual")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível?")

    class Meta:
        verbose_name = "Unidade da Frota"
        verbose_name_plural = "Frota de Veículos"
        ordering = ['veiculo__marca', 'veiculo__modelo']

    def __str__(self):
        return f"{self.veiculo} - {self.placa}"

    @classmethod
    def unidades_disponiveis(cls, veiculo_id=None):
        queryset = cls.objects.filter(disponivel=True)
        if veiculo_id:
            queryset = queryset.filter(veiculo_id=veiculo_id)
        return queryset

    @classmethod
    def verificar_disponibilidade_modelo(cls, veiculo_id):
        return cls.unidades_disponiveis(veiculo_id).count()


class Alocacao(models.Model):
    unidade_frota = models.ForeignKey(
        Frota,
        on_delete=models.PROTECT,
        related_name='alocacoes',
        verbose_name="Unidade da Frota"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='alocacoes',
        verbose_name="Cliente"
    )
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        related_name='alocacoes',
        verbose_name="Setor"
    )
    data_alocacao = models.DateTimeField(
        verbose_name="Data de Alocação"
    )
    data_devolucao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Devolução"
    )
    km_inicial = models.PositiveIntegerField(
        verbose_name="Quilometragem Inicial",
        help_text="Quilometragem no momento da alocação"
    )
    km_final = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Quilometragem Final",
        help_text="Quilometragem no momento da devolução"
    )
    motivo = models.TextField(
        verbose_name="Motivo da Alocação",
        max_length=500
    )
    observacoes = models.TextField(
        verbose_name="Observações",
        blank=True,
        null=True,
        max_length=1000
    )

    class Meta:
        verbose_name = "Alocação"
        verbose_name_plural = "Alocações"
        ordering = ['-data_alocacao']
        indexes = [
            models.Index(fields=['-data_alocacao']),
            models.Index(fields=['unidade_frota', 'data_devolucao']),
        ]

    @property
    def em_uso(self):
        return self.data_devolucao is None

    @property
    def km_percorridos(self):
        if self.km_final and self.km_inicial:
            return self.km_final - self.km_inicial
        return None

    def __str__(self):
        status = "Em uso" if self.em_uso else f"Devolvido em {self.data_devolucao.date()}"
        return f"{self.unidade_frota} alocado para {self.cliente} ({status})"

    def save(self, *args, **kwargs):
        is_new = not self.pk

        if is_new:
            self.unidade_frota.disponivel = False
            self.km_inicial = self.unidade_frota.km_atual
        elif self.data_devolucao and not self.unidade_frota.disponivel:
            self.unidade_frota.disponivel = True
            if self.km_final:
                self.unidade_frota.km_atual = self.km_final

        super().save(*args, **kwargs)

        self.unidade_frota.save()


@receiver(post_delete, sender=Alocacao)
def atualizar_disponibilidade_frota(sender, instance, **kwargs):
    frota = instance.unidade_frota

    if not frota.alocacoes.filter(data_devolucao__isnull=True).exists():
        frota.disponivel = True
        frota.save()
