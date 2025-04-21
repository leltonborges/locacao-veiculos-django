from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Prefetch, Q

from rental.models import Setor, Alocacao
from rental.views.setores.forms import SetorForm


def listar_setores(request):
    setores = Setor.objects.annotate(
        total_alocacoes=Count('alocacoes'),
        alocacoes_ativas=Count('alocacoes', filter=Q(alocacoes__data_devolucao__isnull=True))
    ).all()
    return render(request, 'rental/setores/listar_setores.html', {
        'setores': setores,
        'titulo': 'Lista de Setores'
    })


def criar_setor(request):
    if request.method == 'POST':
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Setor cadastrado com sucesso!')
            return redirect('listar_setores')
    else:
        form = SetorForm()

    return render(request, 'rental/setores/setor_form.html', {
        'form': form,
        'titulo': 'Cadastrar Novo Setor'
    })


def detalhar_setor(request, setor_id):
    setor = get_object_or_404(
        Setor.objects.prefetch_related(
            Prefetch('alocacoes',
                     queryset=Alocacao.objects.select_related(
                         'unidade_frota',
                         'unidade_frota__veiculo',
                         'cliente'
                     ).filter(data_devolucao__isnull=True),
                     to_attr='alocacoes_ativas')
        ),
        pk=setor_id
    )

    return render(request, 'rental/setores/detalhar_setor.html', {
        'setor': setor,
        'titulo': f'Detalhes: {setor.sigla}'
    })


def editar_setor(request, setor_id):
    setor = get_object_or_404(Setor, pk=setor_id)

    if request.method == 'POST':
        form = SetorForm(request.POST, instance=setor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Setor atualizado com sucesso!')
            return redirect('detalhar_setor', setor_id=setor.id)
    else:
        form = SetorForm(instance=setor)

    return render(request, 'rental/setores/setor_form.html', {
        'form': form,
        'titulo': f'Editar: {setor.sigla}'
    })


def deletar_setor(request, setor_id):
    setor = get_object_or_404(Setor, pk=setor_id)

    if request.method == 'POST':
        if setor.alocacoes.count() > 0:
            messages.error(request, 'Não é possível excluir setores com alocações registradas!')
            return redirect('detalhar_setor', setor_id=setor.id)

        setor.delete()
        messages.success(request, 'Setor removido com sucesso!')
        return redirect('listar_setores')

    return render(request, 'rental/setores/confirmar_delete.html', {
        'setor': setor,
        'titulo': f'Confirmar exclusão: {setor.sigla}'
    })
