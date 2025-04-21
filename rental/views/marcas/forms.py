from django import forms

from rental.models import Marca


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome', 'pais_origem', 'fundacao', 'website', 'ativa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'pais_origem': forms.TextInput(attrs={'class': 'form-control'}),
            'fundacao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            'ativa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nome': 'Nome da Marca',
            'pais_origem': 'País de Origem',
            'fundacao': 'Ano de Fundação',
            'website': 'Site Oficial',
            'ativa': 'Marca Ativa',
        }
