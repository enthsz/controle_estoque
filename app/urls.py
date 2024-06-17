from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [

    # AUTENTICAÇAO VIA TOKEN
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    # CRIAR, LISTAR PRODUTOS, ATUALIZAR PRODUTOS, DELETAR PRODUTOS
    path('api/produtos/', views.list_product, name='produtos'),
    path('api/criar-produto/', views.create_product, name='criar-produto'),
    path('api/detalhe-produto/<str:product_name>/', views.product_detail, name='detalhe-produto'),
    path('api/atualizar-produto/<str:product_name>/', views.update_product, name='atualizar-produto'),
    path('api/deletar-produto/<str:product_name>/', views.delete_product, name='deletar-produto'),

    # VENDAS E HISTORICO DE VENDAS
    path('api/vendas/', views.register_sale, name='registrar-venda'),
    path('api/historico_vendas/', views.sales_history, name='historico_vendas'),


]
