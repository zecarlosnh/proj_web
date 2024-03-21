"""
URL configuration for proj_unico_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_unico_web import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ordens/', views.ordens, name='ordens'),
    path('ordens_area/', views.pesquisa_area, name='nome_area'),
    path('preencheos/', views.preencheos, name='cap_os'),
    path('registraos/', views.registraos, name='reg_os'),
    path('iniciaos/', views.registraos, name='iniciaos'),
    path('assina/', views.registraos, name='assina'),
    path('salvaimg/', views.salva_img, name='ass'),
    path('', views.logar, name='logar'),
    path('registrans/',views.registraos, name='reg_ns'),
    path('preencheos/',views.preencheos, name='voltaos'),
    path('ordensretirada/',views.ordensretirada, name='ordensretirada'),
    path('preencheosretirada/',views.preencheosretirada, name='preencheretirada'),
    path('reg_assinado_por/', views.reg_nome_assinatura, name='assinado_por'),
    path('preencheosretirada/',views.preencheosretirada, name='voltar_retirada'),
    path('ordensretirada/', views.ordensretirada, name='pesquisaretirada'),
    path('incluiros/', views.incluiros, name='pesquisacliente'),
    path('incluiros/', views.incluiros, name = 'entidade'),
    path('incluiros/', views.incluiros, name='incluiros'),
    path('confirma_incluir_os/', views.preenche_incluir_os, name='cadastra_os'),
    path('preenche_ordem_abast/', views.preenche_ordem_abast, name= 'preenche_ordem_abast'),
    path('confirma_abast/', views.incluir_ordem_abast, name='abastece'),
    path('imprime_os/', views.imprimir_os, name='imprime_os'), 
    path('login/', views.logar, name='login'),
    path('clientes_ordens/', views.clientes_ordens, name='clientes_ordens'), 
    path('chama_pdf/', views.chama_pdf),
    path('clientes_visualiza_ordens', views.cliente_visualiza_os, name='cliente_consulta_os'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sobre/', views.sobre, name = 'sobre'),
    path('enviar_email/', views.enviar, name = 'envia_email'),
    path('incluir_veiculos/', views.incluir_veiculos, name = 'incluir_veiculos'),
    path('cadastrar_veiculos/',views.cadastrar_veiculos, name='cadastrar'),
    path('incluir_motoristas/', views.incluir_motoristas, name = 'incluir_motoristas'),
    path('cadastrar_motoristas/',views.cadastrar_motoristas, name='cadastrar_motoristas'),
    path('consultar_ordem_abastecimentos/', views.consulta_ordem_abastecimentos, name='consulta_ordem_abastecimentos'),
    path('altera_valor_ordem_abastecimento/', views.altera_valor_ordem_abastecimento, name='altera_valor'),
    path('registra_novo_valor/', views.registra_valor_ordem_abastecimento, name='registra_valor')
    
]
