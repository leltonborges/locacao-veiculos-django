from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from rental.models import Frota
from rental.views.frota.forms import FrotaForm


def listar_frota(request):
    frota = Frota.objects.select_related('veiculo', 'veiculo__marca').all()
    return render(request, 'rental/frota/listar_frota.html', {
        'frota': frota,
        'titulo': 'Lista da Frota'
    })


def criar_frota(request):
    if request.method == 'POST':
        form = FrotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unidade da frota cadastrada com sucesso!')
            return redirect('listar_frota')
    else:
        form = FrotaForm()

    return render(request, 'rental/frota/frota_form.html', {
        'form': form,
        'titulo': 'Cadastrar Nova Unidade'
    })


def detalhar_frota(request, frota_id):
    unidade = get_object_or_404(
        Frota.objects.select_related('veiculo', 'veiculo__marca')
        .prefetch_related('alocacoes', 'alocacoes__cliente'),
        pk=frota_id
    )

    return render(request, 'rental/frota/detalhar_frota.html', {
        'unidade': unidade,
        'titulo': f'Detalhes: {unidade.placa}'
    })


def editar_frota(request, frota_id):
    unidade = get_object_or_404(Frota, pk=frota_id)

    if request.method == 'POST':
        form = FrotaForm(request.POST, instance=unidade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unidade atualizada com sucesso!')
            return redirect('detalhar_frota', frota_id=unidade.id)
    else:
        form = FrotaForm(instance=unidade)

    return render(request, 'rental/frota/frota_form.html', {
        'form': form,
        'titulo': f'Editar: {unidade.placa}'
    })


def deletar_frota(request, frota_id):
    unidade = get_object_or_404(Frota, pk=frota_id)

    if request.method == 'POST':
        unidade.delete()
        messages.success(request, 'Unidade removida com sucesso!')
        return redirect('listar_frota')

    return render(request, 'rental/frota/confirmar_delete.html', {
        'unidade': unidade,
        'titulo': f'Confirmar exclusão: {unidade.placa}'
    })
