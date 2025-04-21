from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AlocacaoForm
from .models import Veiculo, Frota


def home(request):
    return render(request, 'rental/home.html')


def alocar_veiculo(request):
    veiculos = Veiculo.objects.annotate_disponiveis().filter(unidades_disponiveis__gt=0)
    context = {
        'veiculos': veiculos,
    }
    return render(request, 'rental/alocacao/alocar_veiculo.html', context)


def alocar_veiculo_detalhes(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    unidades_disponiveis = Frota.unidades_disponiveis(veiculo_id=veiculo_id)

    if request.method == 'POST':
        form = AlocacaoForm(request.POST)
        if form.is_valid():
            alocacao = form.save(commit=False)
            alocacao.unidade_frota = form.cleaned_data['unidade_frota']
            alocacao.save()
            messages.success(request, f'Veículo {alocacao.unidade_frota} alocado com sucesso!')
            return redirect('home')
    else:
        form = AlocacaoForm(initial={'veiculo': veiculo})
        form.fields['unidade_frota'].queryset = unidades_disponiveis

    context = {
        'veiculo': veiculo,
        'unidades_disponiveis': unidades_disponiveis,
        'form': form,
    }
    return render(request, 'rental/alocacao/alocar_veiculo_detalhes.html', context)
