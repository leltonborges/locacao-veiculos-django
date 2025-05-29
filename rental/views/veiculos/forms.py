from django import forms

from rental.models import Veiculo, Marca


class VeiculoForm(forms.ModelForm):
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.filter(ativa=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Marca'
    )

    class Meta:
        model = Veiculo
        fields = ['modelo', 'marca', 'tipo', 'ano_fabricacao']
        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'ano_fabricacao': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'modelo': 'Modelo do Veículo',
            'tipo': 'Tipo de Veículo',
            'ano_fabricacao': 'Ano de Fabricação',
        }
