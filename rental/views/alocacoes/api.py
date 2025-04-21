from django.http import JsonResponse
from rental.models import Frota

def frota_disponivel_por_veiculo(request, veiculo_id):
    unidades = Frota.unidades_disponiveis(veiculo_id=veiculo_id)
    data = [{
        'id': unidade.id,
        'placa': unidade.placa,
        'km_atual': unidade.km_atual,
        'veiculo': f"{unidade.veiculo.marca} {unidade.veiculo.modelo}"
    } for unidade in unidades]
    return JsonResponse(data, safe=False)

def km_frota(request, frota_id):
    try:
        frota = Frota.objects.get(id=frota_id)
        return JsonResponse({'km_atual': frota.km_atual})
    except Frota.DoesNotExist:
        return JsonResponse({'error': 'Frota não encontrada'}, status=404)