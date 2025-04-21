from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count

from rental.models import Marca
from rental.views.marcas.forms import MarcaForm


def listar_marcas(request):
    marcas = Marca.objects.annotate(
        total_veiculos=Count('veiculos')
    ).all()
    return render(request, 'rental/marcas/listar_marcas.html', {
        'marcas': marcas,
        'titulo': 'Lista de Marcas'
    })


def criar_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca cadastrada com sucesso!')
            return redirect('listar_marcas')
    else:
        form = MarcaForm()

    return render(request, 'rental/marcas/marca_form.html', {
        'form': form,
        'titulo': 'Cadastrar Nova Marca'
    })


def detalhar_marca(request, marca_id):
    marca = get_object_or_404(
        Marca.objects.prefetch_related(
            'veiculos',
            'veiculos__unidades_frota'
        ),
        pk=marca_id
    )

    marca.total_veiculos = marca.veiculos.count()

    return render(request, 'rental/marcas/detalhar_marca.html', {
        'marca': marca,
        'titulo': f'Detalhes: {marca.nome}'
    })


def editar_marca(request, marca_id):
    marca = get_object_or_404(Marca, pk=marca_id)

    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca atualizada com sucesso!')
            return redirect('detalhar_marca', marca_id=marca.id)
    else:
        form = MarcaForm(instance=marca)

    return render(request, 'rental/marcas/marca_form.html', {
        'form': form,
        'titulo': f'Editar: {marca.nome}'
    })


def deletar_marca(request, marca_id):
    marca = get_object_or_404(Marca, pk=marca_id)

    if request.method == 'POST':
        if marca.veiculos.count() > 0:
            messages.error(request, 'Não é possível excluir marcas com veículos cadastrados!')
            return redirect('detalhar_marca', marca_id=marca.id)

        marca.delete()
        messages.success(request, 'Marca removida com sucesso!')
        return redirect('listar_marcas')

    return render(request, 'rental/marcas/confirmar_delete.html', {
        'marca': marca,
        'titulo': f'Confirmar exclusão: {marca.nome}'
    })
