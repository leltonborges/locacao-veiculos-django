from django import forms

from rental.models import Setor


class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome', 'sigla', 'responsavel', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'text-transform:uppercase'
            }),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'setor@empresa.com'
            }),
        }
        labels = {
            'nome': 'Nome do Setor',
            'sigla': 'Sigla (Identificação)',
            'responsavel': 'Responsável',
            'telefone': 'Telefone',
            'email': 'E-mail',
        }
