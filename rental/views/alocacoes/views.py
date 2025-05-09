from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from rental.models import Alocacao, Frota, Cliente, Setor, Veiculo


def listar_alocacoes(request):
    alocacoes = Alocacao.objects.all().order_by('-data_alocacao')
    return render(request, 'rental/alocacao/listar_alocacoes.html', {
        'alocacoes': alocacoes,
        'titulo': 'Lista de Alocações'
    })


def detalhar_alocacao(request, alocacao_id):
    alocacao = get_object_or_404(Alocacao, pk=alocacao_id)

    context = {
        'alocacao': alocacao,
        'titulo': f'Alocação #{alocacao.id}',
        'mostrar_botao_devolver': alocacao.em_uso
    }

    return render(request, 'rental/alocacao/detalhar_alocacao.html', context)


def criar_alocacao(request):
    if request.method == 'POST':
        try:
            unidade_frota = Frota.objects.get(id=request.POST['unidade_frota'])

            if not unidade_frota.disponivel:
                raise ValidationError("Esta unidade da frota não está disponível")

            data_alocacao_str = f"{request.POST['data_alocacao']} {request.POST['hora_alocacao']}"
            data_alocacao = timezone.datetime.strptime(data_alocacao_str, '%Y-%m-%d %H:%M')

            data_devolucao = None
            if request.POST.get('data_devolucao'):
                data_devolucao_str = f"{request.POST['data_devolucao']} {request.POST.get('hora_devolucao', '23:59')}"
                data_devolucao = timezone.datetime.strptime(data_devolucao_str, '%Y-%m-%d %H:%M')

            alocacao = Alocacao.objects.create(
                unidade_frota=unidade_frota,
                cliente_id=request.POST['cliente'],
                setor_id=request.POST['setor'],
                data_alocacao=data_alocacao,
                data_devolucao=data_devolucao,
                motivo=request.POST['motivo'],
                km_inicial=unidade_frota.km_atual,
                km_final=request.POST.get('km_final'),
                observacoes=request.POST.get('observacoes', '')
            )
            alocacao.save()
            return redirect('listar_alocacoes')

        except Exception as e:
            error_message = f"Erro ao criar alocação: {str(e)}"
    else:
        error_message = None

    veiculos_disponiveis = Veiculo.objects.annotate_disponiveis().filter(unidades_disponiveis__gt=0)
    clientes = Cliente.objects.all()
    setores = Setor.objects.all()

    return render(request, 'rental/alocacao/criar_alocacao.html', {
        'veiculos': veiculos_disponiveis,
        'clientes': clientes,
        'setores': setores,
        'error_message': error_message,
        'data_atual': timezone.now().strftime('%Y-%m-%d'),
        'hora_atual': timezone.now().strftime('%H:%M')
    })


def registrar_devolucao(request, alocacao_id):
    alocacao = get_object_or_404(Alocacao, pk=alocacao_id)

    if not alocacao.em_uso:
        messages.error(request, 'Esta alocação já foi devolvida!')
        return redirect('detalhar_alocacao', alocacao_id=alocacao.id)

    if request.method == 'POST':
        try:
            data_devolucao_str = f"{request.POST['data_devolucao']} {request.POST['hora_devolucao']}"
            data_devolucao = timezone.datetime.strptime(data_devolucao_str, '%Y-%m-%d %H:%M')

            km_final = int(request.POST['km_final'])

            if km_final < alocacao.km_inicial:
                raise ValidationError("Quilometragem final não pode ser menor que a inicial")

            alocacao.data_devolucao = data_devolucao
            alocacao.km_final = km_final
            alocacao.observacoes = request.POST.get('observacoes', '')
            alocacao.save()

            messages.success(request, 'Devolução registrada com sucesso!')
            return redirect('detalhar_alocacao', alocacao_id=alocacao.id)

        except Exception as e:
            messages.error(request, f'Erro ao registrar devolução: {str(e)}')

    return render(request, 'rental/alocacao/registrar_devolucao.html', {
        'alocacao': alocacao,
        'titulo': f'Registrar Devolução - {alocacao.unidade_frota}',
        'data_atual': timezone.now().strftime('%Y-%m-%d'),
        'hora_atual': timezone.now().strftime('%H:%M')
    })
