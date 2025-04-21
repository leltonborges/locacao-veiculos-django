from django import forms

from rental.models import Veiculo


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['modelo', 'marca', 'tipo', 'ano_fabricacao']
        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'ano_fabricacao': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'modelo': 'Modelo do Veículo',
            'marca': 'Marca',
            'tipo': 'Tipo de Veículo',
            'ano_fabricacao': 'Ano de Fabricação',
        }
