from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rental.viewsets import (
    MarcaViewSet, VeiculoViewSet, ClienteViewSet,
    SetorViewSet, FrotaViewSet, AlocacaoViewSet
)

router = DefaultRouter()
router.register(r'marcas', MarcaViewSet)
router.register(r'veiculos', VeiculoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'setores', SetorViewSet)
router.register(r'frota', FrotaViewSet)
router.register(r'alocacoes', AlocacaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('', include('rental.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
