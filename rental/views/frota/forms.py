from django import forms
from rental.models import Frota


class FrotaForm(forms.ModelForm):
    class Meta:
        model = Frota
        fields = ['veiculo', 'placa', 'km_atual', 'disponivel']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'AAA-0000'
            }),
            'km_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'disponivel': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'veiculo': 'Modelo do Veículo',
            'placa': 'Placa',
            'km_atual': 'Quilometragem Atual',
            'disponivel': 'Disponível para alocação',
        }
