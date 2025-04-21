from datetime import date
from django.utils import timezone
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django import forms

from .models import Marca, Veiculo, Cliente, Setor, Alocacao, Frota


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        widgets = {
            'telefone': forms.TextInput(attrs={
                'class': 'telefone-mask',
                'placeholder': '(99) 99999-9999'
            }),
            'cnh': forms.TextInput(attrs={
                'class': 'cnh-mask',
                'placeholder': '12345678901'
            }),
        }
        fields = '__all__'


class CNHValidaFilter(admin.SimpleListFilter):
    title = 'CNH válida'
    parameter_name = 'cnh_valida'

    def lookups(self, request, model_admin):
        return (
            ('sim', 'Sim'),
            ('nao', 'Não'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.filter(validade_cnh__gte=date.today())
        if self.value() == 'nao':
            return queryset.filter(validade_cnh__lt=date.today())
        return queryset


class EmUsoFilter(SimpleListFilter):
    title = 'Em uso'
    parameter_name = 'em_uso'

    def lookups(self, request, model_admin):
        return (
            ('sim', 'Sim'),
            ('nao', 'Não'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.filter(data_devolucao__isnull=True)
        if self.value() == 'nao':
            return queryset.filter(data_devolucao__isnull=False)
        return queryset


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'pais_origem', 'fundacao', 'ativa')
    list_filter = ('ativa', 'pais_origem')
    search_fields = ('nome', 'website')


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'marca', 'tipo', 'ano_fabricacao', 'unidades_disponiveis')
    list_filter = ('marca', 'tipo', 'ano_fabricacao')
    search_fields = ('modelo', 'marca__nome')
    ordering = ('marca__nome', 'modelo')
    list_select_related = ('marca',)

    def unidades_disponiveis(self, obj):
        return obj.unidades_frota.filter(disponivel=True).count()

    unidades_disponiveis.short_description = 'Unidades Disponíveis'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm
    list_display = ('nome', 'cnh', 'validade_cnh', 'cnh_valida', 'telefone', 'email', 'alocacoes_ativas')
    list_filter = (CNHValidaFilter,)
    search_fields = ('nome', 'cnh', 'email', 'telefone')
    ordering = ('nome',)
    readonly_fields = ('cnh_valida',)

    def cnh_valida(self, obj):
        return obj.cnh_valida

    cnh_valida.boolean = True
    cnh_valida.short_description = 'CNH Válida'

    def alocacoes_ativas(self, obj):
        return obj.alocacoes.filter(data_devolucao__isnull=True).count()

    alocacoes_ativas.short_description = 'Alocações Ativas'


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'responsavel', 'alocacoes_count')
    search_fields = ('nome', 'sigla', 'responsavel')


@admin.register(Alocacao)
class AlocacaoAdmin(admin.ModelAdmin):
    list_display = (
        'unidade_frota',
        'cliente',
        'setor',
        'data_alocacao',
        'em_uso',
        'km_percorridos'
    )
    list_filter = (
        'setor',
        'unidade_frota__veiculo__marca',
        EmUsoFilter,
        'data_alocacao'
    )
    search_fields = (
        'unidade_frota__placa',
        'unidade_frota__veiculo__modelo',
        'cliente__nome',
        'setor__nome'
    )
    raw_id_fields = ('unidade_frota', 'cliente', 'setor')
    date_hierarchy = 'data_alocacao'
    readonly_fields = ('km_percorridos', 'em_uso', 'data_alocacao')

    fieldsets = (
        (None, {
            'fields': (
                'unidade_frota',
                'cliente',
                'setor',
                'motivo'
            )
        }),
        ('Datas', {
            'fields': (
                'data_devolucao',
            )
        }),
        ('Quilometragem', {
            'fields': (
                'km_inicial',
                'km_final',
                'km_percorridos'
            )
        }),
        ('Outros', {
            'fields': ('observacoes',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj:  # Se estiver editando
            readonly_fields.append('km_inicial')
            readonly_fields.append('data_alocacao')
        else:
            readonly_fields = ['km_percorridos', 'em_uso']
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.data_alocacao = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(Frota)
class FrotaAdmin(admin.ModelAdmin):
    list_display = ('placa', 'veiculo', 'km_atual', 'disponivel', 'em_uso', 'ultima_alocacao')
    list_filter = ('disponivel', 'veiculo__marca', 'veiculo__tipo')
    search_fields = ('placa', 'veiculo__modelo')
    ordering = ('veiculo__marca__nome', 'veiculo__modelo', 'placa')
    list_select_related = ('veiculo__marca',)
    raw_id_fields = ('veiculo',)
    readonly_fields = ('km_atual', 'disponivel')

    def em_uso(self, obj):
        return obj.alocacoes.filter(data_devolucao__isnull=True).exists()

    em_uso.boolean = True
    em_uso.short_description = 'Em Uso'

    def ultima_alocacao(self, obj):
        alocacao = obj.alocacoes.order_by('-data_alocacao').first()
        return alocacao.data_alocacao.date() if alocacao else '-'

    ultima_alocacao.short_description = 'Última Alocação'