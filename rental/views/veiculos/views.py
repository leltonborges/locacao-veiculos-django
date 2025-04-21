from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from rental.models import Veiculo
from rental.views.veiculos.forms import VeiculoForm


def listar_veiculos(request):
    veiculos = Veiculo.objects.select_related('marca').all()
    return render(request, 'rental/veiculos/listar_veiculos.html', {
        'veiculos': veiculos,
        'titulo': 'Lista de Veículos'
    })


def criar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('listar_veiculos')
    else:
        form = VeiculoForm()

    return render(request, 'rental/veiculos/veiculo_form.html', {
        'form': form,
        'titulo': 'Cadastrar Novo Veículo'
    })


def detalhar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(
        Veiculo.objects.select_related('marca').prefetch_related('unidades_frota'),
        pk=veiculo_id
    )

    unidades_frota = veiculo.unidades_frota.all()

    return render(request, 'rental/veiculos/detalhar_veiculo.html', {
        'veiculo': veiculo,
        'unidades_frota': unidades_frota,
        'titulo': f'Detalhes do Veículo: {veiculo}'
    })


def editar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)

    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('listar_veiculos')
    else:
        form = VeiculoForm(instance=veiculo)

    return render(request, 'rental/veiculos/veiculo_form.html', {
        'form': form,
        'titulo': f'Editar Veículo: {veiculo}'
    })
