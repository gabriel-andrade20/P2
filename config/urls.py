from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from loja import views

router = DefaultRouter()
router.register('vendedores', views.VendedorViewSet)
router.register('produtos', views.ProdutoViewSet)
router.register('cupons', views.CupomViewSet)
router.register('pedidos', views.PedidoViewSet)
urlpatterns = [path('', views.loja, name='loja'), path('admin/', admin.site.urls), path('dashboard/', views.dashboard), path('api/', include(router.urls)), path('api-auth/', include('rest_framework.urls'))]
