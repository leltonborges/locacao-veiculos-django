from django import forms
from .models import Alocacao, Frota, Cliente, Setor


class AlocacaoForm(forms.ModelForm):
    class Meta:
        model = Alocacao
        fields = ['unidade_frota', 'cliente', 'setor', 'motivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unidade_frota'].queryset = Frota.objects.none()

        if 'veiculo' in self.initial:
            veiculo = self.initial['veiculo']
            self.fields['unidade_frota'].queryset = Frota.unidades_disponiveis(veiculo_id=veiculo.id)