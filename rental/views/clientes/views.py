from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count

from rental.models import Cliente
from rental.views.clientes.forms import ClienteForm


def listar_clientes(request):
    clientes = Cliente.objects.annotate(
        total_alocacoes=Count('alocacoes')
    ).all()
    return render(request, 'rental/clientes/listar_clientes.html', {
        'clientes': clientes,
        'titulo': 'Lista de Clientes'
    })


def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('listar_clientes')
    else:
        form = ClienteForm()

    return render(request, 'rental/clientes/cliente_form.html', {
        'form': form,
        'titulo': 'Cadastrar Novo Cliente'
    })


def detalhar_cliente(request, cliente_id):
    cliente = get_object_or_404(
        Cliente.objects.prefetch_related(
            'alocacoes',
            'alocacoes__unidade_frota',
            'alocacoes__unidade_frota__veiculo'
        ),
        pk=cliente_id
    )

    cnh_valida = date.today() <= cliente.validade_cnh if cliente.validade_cnh else False

    return render(request, 'rental/clientes/detalhar_cliente.html', {
        'cliente': cliente,
        'cnh_valida': cnh_valida,
        'titulo': f'Detalhes: {cliente.nome}'
    })


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('detalhar_cliente', cliente_id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'rental/clientes/cliente_form.html', {
        'form': form,
        'titulo': f'Editar: {cliente.nome}'
    })


def deletar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == 'POST':
        if cliente.alocacoes.count() > 0:
            messages.error(request, 'Não é possível excluir clientes com alocações registradas!')
            return redirect('detalhar_cliente', cliente_id=cliente.id)

        cliente.delete()
        messages.success(request, 'Cliente removido com sucesso!')
        return redirect('listar_clientes')

    return render(request, 'rental/clientes/confirmar_delete.html', {
        'cliente': cliente,
        'titulo': f'Confirmar exclusão: {cliente.nome}'
    })
