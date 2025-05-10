from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rental.viewsets import (
    MarcaViewSet, VeiculoViewSet, ClienteViewSet,
    SetorViewSet, FrotaViewSet, AlocacaoViewSet
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'marcas', MarcaViewSet)
router.register(r'veiculos', VeiculoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'setores', SetorViewSet)
router.register(r'frota', FrotaViewSet)
router.register(r'alocacoes', AlocacaoViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API de Gerenciamento de Frota",
        default_version='v1',
        description="API para gerenciamento de frota de veículos",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('', include('rental.urls')),
    
    # Swagger URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
