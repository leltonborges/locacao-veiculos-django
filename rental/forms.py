from django import forms
from .models import Alocacao, Frota, Cliente, Setor

from django import forms
from django.forms import DateInput
from .models import Alocacao, Frota


class AlocacaoForm(forms.ModelForm):
    class Meta:
        model = Alocacao
        fields = ['unidade_frota', 'cliente', 'setor', 'motivo', 'data_alocacao']
        widgets = {
            'data_alocacao': DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control datepicker',
                },
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unidade_frota'].queryset = Frota.objects.none()

        if 'veiculo' in kwargs.get('initial', {}):
            veiculo = kwargs['initial']['veiculo']
            self.fields['unidade_frota'].queryset = Frota.unidades_disponiveis(veiculo_id=veiculo.id)

        # Garante que o formato da data seja reconhecido corretamente
        self.fields['data_alocacao'].input_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y']
