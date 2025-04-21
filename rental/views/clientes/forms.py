from django import forms

from rental.models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cnh', 'validade_cnh', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnh': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da CNH'
            }),
            'validade_cnh': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'cnh': 'Número da CNH',
            'validade_cnh': 'Validade da CNH',
            'telefone': 'Telefone',
            'email': 'E-mail',
        }
