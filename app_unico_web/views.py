from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role
from rolepermissions.permissions import revoke_permission, grant_permission
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from django.db import connections
from datetime import datetime, timezone, tzinfo
import base64
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import B7, A4
import os
import subprocess
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import winsound
import pyaudio
import wave
import sys
from pydub import AudioSegment
from pydub.playback import play
import win32print
import win32api
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame, SimpleDocTemplate
from .models import Caminhos_arquivos, Veiculos, Motoristas, Ordem_abastecimento

def som():
    caminho_som = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\erro.wav'
    CHUNK = 1024

    if len(sys.argv) < 2:
        print(f'Plays a wave file. Usage: {sys.argv[0]} {caminho_som}')
        sys.exit(-1)

    with wave.open(caminho_som, 'rb') as wf:
        # Instantiate PyAudio and initialize PortAudio system resources (1)
        p = pyaudio.PyAudio()

        # Open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Play samples from the wave file (3)
        while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
            stream.write(data)

        # Close stream (4)
        stream.close()

        # Release PortAudio system resources (5)
        p.terminate()


# def som():
#     caminho_som = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\erro.wav'
#     sound = AudioSegment.from_wav(caminho_som)
#     play(sound)

# def som():
#     caminho_som = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\erro.wav'
#     chunk = 1024    
    
#     wf = wave.open(caminho_som, 'rb')

#     # Create an interface to PortAudio
#     p = pyaudio.PyAudio()

#     # Open a .Stream object to write the WAV file to
#     # 'output = True' indicates that the sound will be played rather than recorded
#     stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
#                     channels = wf.getnchannels(),
#                     rate = wf.getframerate(),
#                     output = True)

#     # Read data in chunks
#     data = wf.readframes(chunk)

#     # Play the sound by writing the audio data to the stream
#     while data != '':
#         stream.write(data)
#         data = wf.readframes(chunk)

#     # Close and terminate the stream
#     stream.close()
#     p.terminate()

    


# def som():
#     caminho_som = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\erro.wav'
#     RECORD_SECONDS = 5
#     CHUNK = 1024
#     RATE = 44100

#     p = pyaudio.PyAudio()
#     stream = p.open(format=p.get_format_from_width(2),
#                     channels=1 if sys.platform == 'darwin' else 2,
#                     rate=RATE,
#                     input=True,
#                     output=True,
#                     frames_per_buffer=CHUNK)

#     print('* recording')
#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         stream.write(stream.read(CHUNK))
#     print('* done')

#     stream.close()
#     p.terminate()


# Create your views here.
# @has_role_decorator('nit10', redirect_url='/clientes_ordens')

@login_required(login_url='login')
def ordens(request):
    # winsound.Beep(3000, 100)
    # winsound.Beep(1000, 100)
    # winsound.Beep(3000, 100)
    # winsound.Beep(1000, 100)
    
    # som()
    
    # if request.user.is_authenticated:    
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT codigo, nomecliente, problemadescrito, idarea, status FROM ordemservico WHERE (status = 1 AND idarea = 12) OR (status = 1 AND idarea = 1) OR (status = 6 AND idarea = 1) ORDER BY codigo DESC")
    data = cursor.fetchall()
    cursor.close()
    
    lista_ordens = [] 
    for i in data:
        tupla_ordens = ()
        tupla_ordens += (i[0],)
        tupla_ordens += (i[1],)
        tupla_ordens += (i[2],)
        num_idarea = i[3]
        num_status = i[4]
        
        if num_status == 6:
            tupla_ordens += ('AGENDADO',)
            
        elif num_idarea == 1:
            tupla_ordens += ('Campo',)
        elif num_idarea == 12:
            tupla_ordens += ('Remoto',)
        
        x = lista_ordens.append(tupla_ordens)
        
        
    # u = request.user.username
    # print(u)
    # assign_role(request.user, 'clientes')   
    
    # x = User.objects.get()
    # print(x)
        

    return render(request, 'os/ordens.html', {'query' : lista_ordens})
    # return render(request, 'os/login.html')

##############################################################
##############################################################
##############################################################
##############################################################
def pesquisa_area(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nome_area = request.POST.get('area')
            print(nome_area)
            if nome_area == 'Campo':
                
                               
                cursor = connections['unico'].cursor()
                cursor.execute("SELECT codigo, nomecliente, problemadescrito FROM ordemservico WHERE (status = 1) AND (idarea = 1) ORDER BY codigo DESC")
                data = cursor.fetchall()
                cursor.close() 
                
                lista_ordens = [] 
                for i in data:
                    tupla_ordens = ()
                    tupla_ordens += (i[0],)
                    tupla_ordens += (i[1],)
                    tupla_ordens += (i[2],)
                    tupla_ordens += ('campo',)
                    x = lista_ordens.append(tupla_ordens)
                    
                # print(tupla_ordens)
                print(lista_ordens) 
                
                
                return render(request, 'os/ordens.html', {'query' : lista_ordens})
            if nome_area == 'Remoto':
                cursor = connections['unico'].cursor()
                cursor.execute("SELECT codigo, nomecliente, problemadescrito FROM ordemservico WHERE (status = 1) AND (idarea = 12) ORDER BY codigo DESC")
                data = cursor.fetchall()
                cursor.close()
                
                lista_ordens = [] 
                for i in data:
                    tupla_ordens = ()
                    tupla_ordens += (i[0],)
                    tupla_ordens += (i[1],)
                    tupla_ordens += (i[2],)
                    tupla_ordens += ('Remoto',)
                    x = lista_ordens.append(tupla_ordens)
            
                # print(tupla_ordens)
                print(lista_ordens) 
                
                
                
                return render(request, 'os/ordens.html', {'query' : lista_ordens})
            
            # if nome_area == 'AGENDADA':
            #     cursor = connections['unico'].cursor()
            #     cursor.execute("SELECT codigo, nomecliente, problemadescrito FROM ordemservico WHERE (status = 6) AND (idarea = 1) AND (idarea = 1) ORDER BY codigo DESC")
            #     data = cursor.fetchall()
            #     cursor.close()
                
            #     lista_ordens = [] 
            #     for i in data:
            #         tupla_ordens = ()
            #         tupla_ordens += (i[0],)
            #         tupla_ordens += (i[1],)
            #         tupla_ordens += (i[2],)
            #         tupla_ordens += ('Remoto',)
            #         x = lista_ordens.append(tupla_ordens)
            
            #     # print(tupla_ordens)
            #     print(lista_ordens) 
                
                
                
                # return render(request, 'os/ordens.html', {'query' : lista_ordens})
            
            
            
    return render(request, 'os/login.html')   
##############################################################
##############################################################
##############################################################
##############################################################
def preencheos(request):
    if request.user.is_authenticated:
        os = {
            'num_os' : request.POST.get('subject')
        }
        cursor = connections['unico'].cursor()
        cursor.execute("SELECT codigo, nomecliente, problemadescrito, idcliente FROM ordemservico WHERE (codigo = %i)" % (int(os['num_os'])))
        data = cursor.fetchall()
        cursor.close()
        
        
        idcliente = ''
    
        tuple_nova = ()
        
        for i in data:
            idcliente = i[3]
            tuple_nova += i
        
        
        
        
        cursor = connections['unico'].cursor()
        cursor.execute("SELECT nome, endereco, numeroendereco, idcidade FROM entidade WHERE (id = %i)" % int(idcliente))
        nome_fantasia = cursor.fetchall()
        cursor.close()
        
        
        resultado_fantasia = ''
        resultado_end = ''
        resultado_num_end = ''  
        id_cidade = '' 
        for i in nome_fantasia:
            resultado_fantasia = i[0]
            resultado_end = i[1]
            resultado_num_end = i[2]
            id_cidade = i[3]
            
        cursor = connections['unico'].cursor()
        cursor.execute("SELECT nome FROM cidade WHERE (id = %i)" % int(id_cidade))
        nome_cidade = cursor.fetchall()   
        cursor.close()
        resultado_cidade = ''
        for i in nome_cidade:
            resultado_cidade = i[0]
            
        endereco = (f'{resultado_end}, {resultado_num_end}, {resultado_cidade}')
        
        tuple_nova += (resultado_fantasia, endereco,)
        
        
        cursor = connections['unico'].cursor()
        cursor.execute("SELECT extra6, servicoexecutado FROM ordemservico WHERE (codigo = %i)" % (int(os['num_os'])))
        ja_preenchido = cursor.fetchall()
        cursor.close()
        hora_chegada = ''
        servico_preenchido = ''
        
        for i in ja_preenchido:
            hora_chegada = i[0]
            servico_preenchido = i[1]
        tuple_nova += (hora_chegada, servico_preenchido,)   
        
        
        # tuple_nova += (hora_chegada)
        
        cursor = connections['unico'].cursor()
        cursor.execute("SELECT numerofabricacao FROM ordemservico WHERE (codigo = %i)" % (int(os['num_os'])))
        ns = cursor.fetchall()
        cursor.close()
        resultado_ns = ''
        for i in ns:
            resultado_ns = i[0]
        tuple_nova += (resultado_ns,)
            
        
        lista_tuple = [tuple_nova]
        
        print(lista_tuple)
            
        return render(request, 'os/preencheos.html', {'query' : lista_tuple})    
    return render(request, 'os/login.html')

##############################################################
##############################################################
##############################################################
##############################################################

def registrans(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            os_num ={'os' : request.POST.get('subject')}
            # print(os_num)
            # resultado_os = ''
            # resultado_nuos = ''
            # for i,x in os_num.items():
            #     resultado_os =i
            #     resultado_nuos = x
            # print(resultado_os)
            # print(resultado_os)
            
            
            return render(request, 'os/ordens.html')
            
    return render(request, 'os/login.html')      





##############################################################
##############################################################
##############################################################
##############################################################

def registraos(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            
            verifica_post = {'post' : request.POST.get('regserv')}
            post = str(verifica_post['post'])
            data_e_hora_atuais = datetime.now()
            data_str = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
            imprime = request.POST.get('imprime')
            
            print(imprime)
            if post == 'reg':
                
                enc_encerramento = 'PYTHON'
                os_num ={'os' : request.POST.get('subject')}
                serv_executado = request.POST.get('servicoexecutado').upper()
                nomeass = request.POST.get('nome_ass').upper()
                if nomeass != '':
                    
                    # registrans = (f'{serv_executado}. ASSINADO POR: {nomeass}')
                    cursor = connections['unico'].cursor()
                    cursor.execute("UPDATE ordemservico SET servicoexecutado = '%s', extra4 = 'PYTHON', extra7 = '%s', extra12 = '%s' WHERE codigo = %i" % (serv_executado, data_str, nomeass, int(os_num['os'])))
                    cursor.close()
                    
                    return render(request, 'os/assina.html', os_num)
                else:
                    return HttpResponse('INFORME O NOME DE QUEM ASSINARÁ!!!')
            
            if post == 'inicia':

                os_num ={'os' : request.POST.get('inicia')}
                
                
                cursor = connections['unico'].cursor()
                cursor.execute("UPDATE ordemservico SET extra6 = '%s' WHERE codigo = %i" % (data_str, int(os_num['os'])))
                cursor.close()   
                
                cursor = connections['unico'].cursor()
                cursor.execute("SELECT codigo, nomecliente, problemadescrito, idarea FROM ordemservico WHERE (status = 1 AND idarea = 12) OR (status = 1 AND idarea = 1) ORDER BY codigo DESC")
                data = cursor.fetchall()
                cursor.close()
                
                # lista_ordens = [] 
                # for i in data:
                #     tupla_ordens = ()
                #     tupla_ordens += (i[0],)
                #     tupla_ordens += (i[1],)
                #     tupla_ordens += (i[2],)
                #     num_idarea = i[3]
                #     if num_idarea == 1:
                #         tupla_ordens += ('Campo',)
                #     if num_idarea == 12:
                #         tupla_ordens += ('Remoto',) 
                #     x = lista_ordens.append(tupla_ordens)
                
                       
                return render(request, 'os/iniciaos.html')
            
            
            if post == 'assina':
                os_num ={'os' : request.POST.get('assina')}
                print(os_num)
                return render(request, 'os/assina.html', os_num)
            
            if post == 'regns':
                os_num ={'os' : request.POST.get('num_regos')}
                registrans = request.POST.get('registrans').upper()
                cursor = connections['unico'].cursor()
                cursor.execute("UPDATE ordemservico SET numerofabricacao = '%s' WHERE codigo = %i" % (registrans, int(os_num['os'])))
                cursor.close()
                
                
            
            
                resultado_os = ''
                resultado_nuos = ''
                for i,x in os_num.items():
                    resultado_os =i
                    resultado_nuos = str(x)
        
                tuple_os = ()
                tuple_os += (resultado_nuos,)
                
                list_os = [tuple_os]
            
                
                return render(request, 'os/registrans.html', {'query' : list_os})
    return render(request, 'os/login.html')     
##############################################################
##############################################################
##############################################################
##############################################################

        
             
def salva_img(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            system_state = 'dev'
            caminho_salva_img = {'caminho': Caminhos_arquivos.objects.filter(nome = system_state).values()}
            for i in caminho_salva_img['caminho']:
                consulta_caminho = i['assinaturas']
                
            
            # y = caminho_salva_img.get('caminho')
            # print(y['prod'])
            # print(caminho_salva_img['caminho'])
            caminho_arquivo = consulta_caminho
            # caminho_arquivo = 'C:\\unicoweb\\proj_unico_web\\app_unico_web\\assinaturas\\'
            
        
            os_num ={'os' : request.POST.get('osnum')}
            x = os_num.get('os')
            # str_os = str(x)
            # str_os += '.png'
            
            caminho_arquivo += str(x)
            caminho_arquivo += '.png'
            
        
            
            img = {'i': request.POST.get('teste')}
            
            str_img = img.get('i')
                
            corte = str_img[21:]
        
        
        
            with open(caminho_arquivo, "wb") as fh:
                fh.write(base64.urlsafe_b64decode(corte))
                

        
            return render(request, 'os/salvaimg.html', os_num)
    return render(request, 'os/login.html') 
##############################################################
##############################################################
##############################################################
##############################################################
   
def logar(request):
    if request.method == "GET":
        return render(request, 'os/login.html')
    else:
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario:
            login(request, usuario)
            return HttpResponseRedirect('ordens/') 
        else:
            return HttpResponse('deu ruim') 
        
        
        
        
        
        
        ##############################################################
##############################################################
##############################################################
##############################################################
def ordensretirada(request):
    if request.user.is_authenticated:
        cursor = connections['unico'].cursor()
        cursor.execute("SELECT codigo, nomecliente, extra11, descricaoitem FROM ordemservico WHERE (extra4 = 'Ag. Retirada') ORDER BY codigo DESC")
        data = cursor.fetchall()
        
        cursor.close()
        if request.method == 'POST':
            pesquisa = request.POST.get('pesquisa').upper()
            
                
                
            print(pesquisa)
            lista_pesquisa = []
            # tupla_nome =()
            for i in data:
                nome = i[1]
                if nome != None:
                    contem = nome.startswith(pesquisa)
                    
                    if contem:
                        lista_pesquisa += (i,)
                else:
                    pass
            
            return render(request, 'os/ordensretirada.html', {'query' : lista_pesquisa})
        return render(request, 'os/ordensretirada.html', {'query' : data})
        
    return render(request, 'os/login.html') 
        # print(tupla_nome)                   


def preencheosretirada(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
        
            os_num ={'os' : request.POST.get('assina')}
            
            cursor = connections['unico'].cursor()
            cursor.execute("SELECT codigo, nomecliente, servicoexecutado, valorprodutos, valorservicos, extra12 FROM ordemservico WHERE (codigo = %i)" % (int(os_num['os'])))
            data = cursor.fetchall()
            cursor.close()
            
            tuple_data = ()
            for i in data:
                codigo = i[0]
                nome_cliente = i[1]
                servicoexecutado = i[2]
                valor_servico = i[4]
                valor_produto = i[3]
                assinado_por = i[5]
            print(data)  
            total_valor = valor_produto + valor_servico
            tuple_data += (codigo,nome_cliente, servicoexecutado, total_valor,)
        
            list_data = [tuple_data]
            
            
            
            
            return render(request, 'os/preencheosretirada.html',{'query' : list_data})
        
   
    return render(request, 'os/login.html') 

def reg_nome_assinatura(request):
    if request.method == 'POST':
        num_os = request.POST.get('assina')
        assinado_por = request.POST.get('nome_ass')
        print(assinado_por)
        cursor = connections['unico'].cursor()
        cursor.execute("UPDATE ordemservico SET extra12 = '%s' WHERE codigo = %i" % (assinado_por, int(num_os)))
        cursor.close()
        # print(num_os)
        # print(type(num_os))
        
        # cursor = connections['unico'].cursor()
        # cursor.execute("SELECT codigo, nomecliente, servicoexecutado, valorprodutos, valorservicos FROM ordemservico WHERE (codigo = %i)" % (int(num_os)))
        # data = cursor.fetchall()
        # cursor.close()
        
        # tuple_data = ()
        # for i in data:
        #     codigo = i[0]
        #     nome_cliente = i[1]
        #     servicoexecutado = i[2]
        #     valor_servico = i[4]
        #     valor_produto = i[3]
            
        # total_valor = valor_produto + valor_servico
        # tuple_data += (codigo,nome_cliente, servicoexecutado, total_valor,)
    
        # list_data = [tuple_data]
        
        
        
        
        return render(request, 'os/reg_assinado_por.html',{'query' : num_os})







def incluiros(request):
    if request.user.is_authenticated:
        
        cliente_selecionado = []
        
        
        if request.method == 'POST':
            
            verifica_post = {'post' : request.POST.get('regserv')}
            post = str(verifica_post['post'])
            data_e_hora_atuais = datetime.now()
            
            data_str = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
            
            if post == 'pesquisa_nome_entidade':
                pesquisa_entidade = request.POST.get('pesquisa').upper()

                
                cursor = connections['unico'].cursor()
                cursor.execute("SELECT nome, razaosocial, cnpjcpf, id FROM entidade")
                entidades = cursor.fetchall()
                cursor.close()
                
            
                lista_entidades = []
                for i in entidades:
                    nome = i[0]
                    if nome != None:
                        contem = nome.startswith(pesquisa_entidade)
                        
                        if contem:
                            lista_entidades += (i,)
                    else:
                        pass
                print(lista_entidades)
            
                return render(request, 'os/incluiros.html', {'query' : lista_entidades})
            
            if post == 'incluir_entidade':
                cnpj_cpf = request.POST.get('incluirentidade')
                print('##########')
                
                cursor = connections['unico'].cursor()
                cursor.execute("SELECT nome, razaosocial, cnpjcpf, id FROM entidade WHERE cnpjcpf = '%s'" %(cnpj_cpf))
                entidades = cursor.fetchall()
                cursor.close()
                
                
                # for i in lista_entidades:
                #     cnpj_lista = i[2]
                #     print('lista cnpj')
                #     print(cnpj_lista)
                #     if i[2] == cnpj_cpf:
                #         print(i)
                #         cliente_selecionado += [i]
                print('oiiiii')
                # print(cliente_selecionado)
                return render(request, 'os/preenche_incluir_os.html', {'query' : entidades})
                
            
            
            
            
        return render(request, 'os/incluiros.html', {'query' : cliente_selecionado})
    return render(request, 'os/login.html') 


def preenche_incluir_os(request):
    if request.user.is_authenticated:
      
      
        if request.method == 'POST':
            
            cnpj_cpf = request.POST.get('cnpjcpf')
           
            id_cliente = request.POST.get('id')
           
            
            nome_area = request.POST.get('id')
            
            
            agendar = request.POST.get('agendar')
            
            descricao_item = request.POST.get('descricao_item').upper()
            
            problema_descrito = request.POST.get('problema_descrito').upper()
            
            nome_cliente = request.POST.get('nome_cliente')
           
            id_atendente = 3784
            cursor = connections['unico'].cursor()
            cursor.execute("SELECT codigo FROM ordemservico ORDER BY codigo DESC")
            os = cursor.fetchone()
            cursor.close()
            
            lista_tupla = [os]
            for i in lista_tupla:
                num_os = i[0]
            num_os += 1
           
            id_filial = 1
            
            id_preioridade = 2
            
            existe_evento = 0
            titulo_dav = 'ORDEM SERVICO'
            cnpj_filial = cnpj_cpf
            
            
            nome_area = request.POST.get('area')
            print(nome_area)
            
            if nome_area =='Escolher...':
                return HttpResponse('ERRO NO PREENCHIMENTO DA OS')
            
            if descricao_item == '' or problema_descrito == '':
                return HttpResponse('ERRO NA DESCRICAO DO ITEM')
        
            
            data_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_os = datetime.now().strftime('%Y-%m-%d')
            if nome_area == 'Campo':
                id_area = 1
                cursor = connections['unico'].cursor()
                cursor.execute("INSERT into ordemservico(idcliente, data, idfilial, cnpjcpfcliente, descricaoitem,problemadescrito,nomecliente,idatendente,codigo,idarea,idprioridade,existeevento,titulodav, cnpjfilial) VALUES (%i,'%s', %i,'%s','%s','%s','%s',%i, %i,%i,%i,%i,'%s','%s')" %(int(id_cliente), data_timestamp, id_filial, cnpj_cpf, descricao_item, problema_descrito, nome_cliente, id_atendente, num_os,id_area,id_preioridade,existe_evento,titulo_dav,cnpj_filial))      
                cursor.close()
            if nome_area == 'Remoto':
                id_area = 12
                cursor = connections['unico'].cursor()
                cursor.execute("INSERT into ordemservico(idcliente, data, idfilial, cnpjcpfcliente, descricaoitem,problemadescrito,nomecliente,idatendente,codigo,idarea,idprioridade,existeevento,titulodav, cnpjfilial) VALUES (%i,'%s', %i,'%s','%s','%s','%s',%i, %i,%i,%i,%i,'%s','%s')" %(int(id_cliente), data_timestamp, id_filial, cnpj_cpf, descricao_item, problema_descrito, nome_cliente, id_atendente, num_os,id_area,id_preioridade,existe_evento,titulo_dav,cnpj_filial))      
                cursor.close()
            
            
                
            
            cursor = connections['unico'].cursor()
            cursor.execute("UPDATE ordemservico SET servicoexecutado = '', serviconaoexecutado = '', caracteristicas = '', status = 1, valor = 0, localatendimento = 0, tipogarantia = 0, garantia = 0 WHERE codigo = %i" % (int(num_os)))
            cursor.close()
            cursor = connections['unico'].cursor()
            cursor.execute("UPDATE ordemservico SET numeronotafiscal = '', deslocamento =  '', extra1 = '', extra2 = '', extra3 = '', extra4 = '', extra5 = '', extra6 = '',extra7 = '',extra8 = '',extra9 = '',extra10 = '', dataos = '%s' WHERE codigo = %i" % (data_os, (int(num_os))))
            cursor.close()
           
            cursor = connections['unico'].cursor()
            cursor.execute("UPDATE ordemservico SET ecfserie = '', ecfmfadicional =  '', ecftipo = '', ecfmarca = '', ecfmodelo = '', coo = 0, numerofabricacao = '', ccf = 0, hash = 0, currenttimemillis = 0, valorprodutos=0, valorservicos=0, valorbrinde = 0, geroufinanceiro = 0, observacao = '', laudotecnico = '', marca = '', modelo = '', anofabricacao = 0, placa = '', renavam = '', faturouparacupom = 0, faturouparanota = 0  WHERE codigo = %i" % (int(num_os)))
            cursor.close()
            
            
            if agendar == 'on':
                
           
                data = request.POST.get('data')
                print(type(data))
                hora = request.POST.get('hora')
                print(type(hora))
                data_e_hora_str = (f'{data} {hora}')
                data_date = datetime.strptime(data_e_hora_str, '%Y-%m-%d %H:%M')
                print(data_date)
                print(type(data_date))
                cursor = connections['unico'].cursor()
                cursor.execute("UPDATE ordemservico SET status = 6, agendamento = '%s' WHERE codigo = %i" % (data_date, int(num_os)))
                cursor.close()
                
            
            return render(request, 'os/confirma_incluir_os.html')  
    return render(request, 'os/login.html') 

@login_required(login_url='login')
@has_role_decorator('abastecimento')
def preenche_ordem_abast(request):
    # if request.user.is_authenticated:
    # imprimir_os(1)
    

    
    
    veiculos_db = {'veiculo' : Veiculos.objects.all().values()}
    motoristas_db = {'motorista' : Motoristas.objects.all().values()}
        
    dados_abastecimento = {}
    dados_abastecimento.update(veiculos_db)
    dados_abastecimento.update(motoristas_db)
      
    # caminho_motoristas = 'C:\\Users\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\veiculos.txt'
    # dados_ordem = {}
    # with open(caminho_motoristas, 'r') as arquivo:
    #     veiculo = []
        
    #     for linha in arquivo:
            
    #         l_veiculo = linha.strip().split()
    #         # print(l_veiculo)
    #         x = tuple(l_veiculo)
            
    #         y = veiculo.append(x)               
    #     print(veiculo)
    #     dados_ordem.update({'veiculos': veiculo})
    
    # caminho_motoristas = 'C:\\Users\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\motoristas.txt'
    # with open(caminho_motoristas, 'r') as arquivo:
    #     motoristas = []
    #     for i in arquivo:
    #         l_motoristas = i.strip().split()
    #         y = motoristas.append(l_motoristas)
        
    #     dados_ordem.update({'motoristas': motoristas})
    #     print(motoristas)
    
    
    
    
    return render(request, 'os/preenche_ordem_abast.html', dados_abastecimento)  
        
    # return render(request, 'os/login.html') 



@login_required(login_url='login')
# @has_role_decorator('clientes')
def incluir_ordem_abast(request):

    # if request.user.is_authenticated:
    if request.method == 'POST':
        
        # caminho_motoristas = 'C:\\Users\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\numero_ordem_abast.txt'
        # with open(caminho_motoristas, 'r') as arquivo:
        #     n_ordem = int(arquivo.readline())
        # print(n_ordem)
        # n_ordem += 1
        # print(n_ordem)

        consulta_ordem_abast = {'ordens' : Ordem_abastecimento.objects.all().values().order_by('-id')}
        lista_ordens = []
        for i in consulta_ordem_abast['ordens']:
            lista_ordens.append(i['numero'])
    
        ultima_ordem = int(lista_ordens[0])
        
        ultima_ordem += 1
        valor = request.POST.get('valor')
        if valor == '':
            valor = 'COMPLETAR'        

        nova_ordem_abastecimento = Ordem_abastecimento()
        nova_ordem_abastecimento.numero = ultima_ordem
        nova_ordem_abastecimento.veiculo = request.POST.get('veiculo').upper()
        nova_ordem_abastecimento.motorista = request.POST.get('motorista').upper()
        nova_ordem_abastecimento.valor = valor
        nova_ordem_abastecimento.data = datetime.now()
        nova_ordem_abastecimento.save()
        
        

        # with open(caminho_motoristas, 'w') as arquivo:
        #     arquivo.write(str(n_ordem))
            
        motorista = request.POST.get('motorista')

        veiculo = request.POST.get('veiculo')
        
        # if valor == '':
        #     valor = 'COMPLETAR'
            
        if motorista != 'Escolher...' and veiculo != 'Escolher...':
            
            system_state = 'dev'
            caminho_padrao = {'caminho': Caminhos_arquivos.objects.filter(nome = system_state).values()}
            for i in caminho_padrao['caminho']:
                consulta_caminho = i['caminhopadrao']
            print(consulta_caminho)
            caminho = consulta_caminho
            caminho += 'teste.pdf'
            caminho_logo = consulta_caminho
            caminho_logo += 'logonit.jpg'
            
            gera_ordem_abastecimento(ultima_ordem, motorista,veiculo, valor, caminho_logo)                    
           
            
            # subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe','/n','C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\teste.pdf'], close_fds=True)
            # subprocess.Popen(['start','chrome','/n','file://192.168.0.226/proj_unico_web/teste.pdf'], shell=True, close_fds=True)
            
            
           
            # consulta_caminho = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\teste.pdf'
            
            
            return chama_pdf(caminho)
            
            # return render(request, 'os/confirma_abast.html')
        else:
            return HttpResponse('INFORME O MOTORISTA e / ou  VEICULO!!!!!')

    # return render(request, 'os/login.html') 

def gera_ordem_abastecimento(numero_ordem_abastecimento, motorista, veiculo, valor, caminho_logo):
    pdfmetrics.registerFont(TTFont('Berlin', 'C:\\Windows\\Fonts\\Arial.ttf'))
    cnv = canvas.Canvas("teste.pdf", pagesize=B7)
    # caminho_arquivo = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\'
    # caminho_arquivo += 'logonit.jpg'
    cnv.drawImage(caminho_logo, 80, 320, width=80, height=40)
    # cnv.setFont('Arial', 14)
    cnv.drawString(30, 300, 'POSTAÇO NOVO HAMBURGO')

    cnv.drawString(20, 280, 'Numero Ordem Abastecimento:')
    cnv.drawString(195, 280, str(numero_ordem_abastecimento))
    cnv.drawString(5, 240, 'Motorista:')
    cnv.drawString(60, 240, motorista)
    cnv.drawString(5, 220, 'Veiculo:')
    cnv.drawString(60, 220, veiculo)
    # cnv.drawString(150, 240, 'Placa:')
    # cnv.drawString(190, 240, placa)
    
    cnv.drawString(5, 200, 'VALOR:')
    cnv.drawString(60, 200, valor)
    
    cnv.rect(10,120,220,70)
    # cnv.set(size=8)
    # cnv.drawString(25, 195, 'CARIMBO:')
    
    
    # cnv.line(20, 150, 230, 150)
    # cnv.drawString(30, 138, 'MANUTEC INFORMÁTICA LTDA')
    
    
    cnv.save()
    return()


def chama_pdf(caminho):
    
    # caminho = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\teste.pdf'
    with open(caminho, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
        return response
    

def imprimir_os(request):
    numero_os = request.POST.get('imprime')
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT nomecliente, problemadescrito, servicoexecutado, extra6, extra7, valorprodutos, valorservicos, cnpjcpfcliente, extra12 FROM ordemservico WHERE (codigo = %i)" % (int(numero_os)))
    data = cursor.fetchall()
    cursor.close()
    for i in data:
        nome_cliente = i[0]
        problema_descrito = i[1]
        servico_executado = i[2]
        data_inicio = i[3]
        data_fim = i[4]
        valor_produtos = i[5]
        valor_servicos = i[6]
        cnpjcpf = i[7]
        assinado_por = i[8]
    
    system_state = 'dev'
    caminho_padrao = {'caminho': Caminhos_arquivos.objects.filter(nome = system_state).values()}
    for i in caminho_padrao['caminho']:
        consulta_caminho = i['caminho_os']
        consulta_caminho_logonit = i['caminhopadrao']
        consulta_caminho_assinaturas = i['assinaturas']
    print(consulta_caminho)
    consulta_caminho_logonit += 'logonit.jpg'
       
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT razaosocial, email FROM entidade WHERE cnpjcpf = '%s'" %(cnpjcpf))
    consulta_entidade = cursor.fetchall()
    cursor.close()   
    for x in consulta_entidade:
        email = x[1]
    
    confeccionar_os_pdf(numero_os, nome_cliente, problema_descrito, servico_executado, data_inicio, data_fim, 
                        valor_produtos, valor_servicos, email, assinado_por, consulta_caminho_logonit, consulta_caminho_assinaturas)
    # arquivo_imprimir = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web'
    
    # caminho = r'C:\Users\ZeCar\Documents\projetos_python\unico_web_60\venv\proj_unico_web\os.pdf'
    
 
    
    return chama_pdf(consulta_caminho)
    
    # envia_email('zecarlosnh@gmail.com')
    
    return render(request, 'os/imprimir_os.html')



def confeccionar_os_pdf(num_os, nome, problema, servico, data_inicio, data_fim, valor_produtos,
                        valor_servicos, email, assinado_por, consulta_caminho_logo, consulta_caminho_assinaturas):
    total_valor = valor_servicos + valor_produtos
    str_val_produto = str(valor_produtos)
    str_val_servico = str(valor_servicos)   
    str_total_valor = str(total_valor)
    data = datetime.now().strftime('%d/%m/%Y')
    
    pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\Arial.ttf'))
    cnv = canvas.Canvas("os.pdf", pagesize=A4)
    # caminho_arquivo = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\'
    # caminho_arquivo += 'logonit.jpg'
    cnv.drawImage(consulta_caminho_logo, 15, 760, width=200, height=90)
    cnv.setFont('Arial', 20)
    cnv.drawString(150, 730, 'ORDE DE SERVIÇO:')
    cnv.drawString(350, 730, num_os)
    
    cnv.setFont('Arial', 14)
    cnv.rect(20,600,550,90)
    cnv.drawString(25, 670, 'MANUTEC INFORMATICA LTDA')
    cnv.setFont('Arial', 12)
    cnv.drawString(25, 650, 'AV. PRIMEIRO DE MARÇO, 2987 - NOVO HAMBURGO - RS - CEP: 93.332-043')
    cnv.drawString(25, 630, 'Fone: 051 3035-2020 - E-mail: contato@NIT10.com.br')
    cnv.drawString(25, 610, 'CNPJ: 08.186.211/0001-72 - I E: 086/0385884')
    
    cnv.rect(20,520,550,50)
    cnv.setFont('Arial', 10)
    cnv.drawString(20, 571, 'DADOS DO CLIENTE: ')
    cnv.setFont('Arial', 16)
    cnv.drawString(25, 550, nome)
    cnv.setFont('Arial', 12)
    cnv.drawString(25, 530, email)
    
    # cnv.rect(20,387,550,100)
    cnv.setFont('Arial', 10)
    cnv.drawString(20, 491, 'DEFEITO INFORMADO:')
    cnv.setFont('Arial', 12)
    # cnv.drawString(25, 470, problema)
    # teste = 'teu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu\n cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cu teu cuteu \ncuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu \ncuteu cuteu cuteu cuteu cuteu cuteu cu teu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu \ncuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cu teu cuteu \ncuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu \ncuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cuteu cu'
    # cnv.rect(20,227,550,130)
    cnv.setFont('Arial', 10)
    cnv.drawString(20, 361, 'SOLUÇÃO DO PROBLEMA:')
    cnv.setFont('Arial', 12)
    # cnv.drawString(25, 340, teste)
    
    # cnv.drawString(25, 200, 'HORA E DATA DE INICIO: ')
    # cnv.drawString(173, 200, data_inicio)
    # cnv.drawString(25, 180, 'HORA E DATA FINAL: ')
    # cnv.drawString(173, 180, data_fim)
    
    cnv.line(150, 60, 400, 60)
    cnv.line(20, 60, 120, 60)
    consulta_caminho_assinaturas += num_os
    consulta_caminho_assinaturas += '.png'
    # caminho_ass= 'C:\\Users\\ZeCar\\Documents\\python_arquivos\\'
    # caminho_ass += num_os
    # caminho_ass += '.png'
    # cnv.drawInlineImage(caminho_ass, 15, 80, width=920, height=250)
    cnv.drawImage(consulta_caminho_assinaturas, 130, 80, width=280, height=100, mask='auto')
    cnv.drawString(180, 40, 'ASSINATURA DO CLIENTE')
    cnv.drawString(460, 60, 'DATA:')
    cnv.drawString(500, 60, data)
   
   
    cnv.drawString(22, 40, 'ASSINADO POR:')
    cnv.drawString(30, 65, assinado_por)
   
    cnv.drawString(380, 200, 'VALOR DOS PRODUTOS: ')
    cnv.drawRightString(566, 200, str_val_produto)
    cnv.drawString(385, 180, 'VALOR DOS SERVIÇOS: ')
    cnv.drawRightString(566, 180, str_val_servico)
    cnv.drawString(438, 160, 'VALOR TOTAL:')
    cnv.drawRightString(566, 160, str_total_valor)   
    
    
    # my_Style=ParagraphStyle('My Para style',
    # fontName='Times-Roman',
    # backColor='#F1F1F1',
    # fontSize=12,
    # borderColor='#FFFF00',
    # borderWidth=2,
    # borderPadding=(20,20,20),
    # leading=20,
    # alignment=0
    # )
    # p1 = Paragraph(servico, my_Style)
    # p1.wrapOn(cnv,510,1)
    # p1.drawOn(cnv,40,100)    
    f_servico = servico.replace('\n','<br/>')
    
    lista_servico = []
    styles = getSampleStyleSheet()
    p_text = Paragraph(f_servico, style=styles["Normal"])
    lista_servico.append(p_text)
    frame = Frame(20,225,550,130, showBoundary=1)
    frame.addFromList(lista_servico, cnv)
    
    
    f_problema = problema.replace('\n','<br/>')
    lista_problema = []
    styles = getSampleStyleSheet()
    p_text = Paragraph(f_problema, style=styles["Normal"])
    lista_problema.append(p_text)
    frame = Frame(20,388,550,100, showBoundary=1)
    frame.addFromList(lista_problema, cnv)
    
    
    cnv.save()
    
    # lista_impressoras = win32print.EnumPrinters(2)
    
    # impressora = lista_impressoras[5]
    # win32print.SetDefaultPrinter(impressora[2])
    
    # arquivo_imprimir = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web'
    
    # win32api.ShellExecute(0, "print", 'os.pdf', None, arquivo_imprimir, 0)
    # caminho = r'C:\Users\ZeCar\Documents\projetos_python\unico_web_60\venv\proj_unico_web\os.pdf'
    # chama_pdf(caminho)
        
    # subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe','/n','C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\os.pdf'], close_fds=True)
    
    

def imprime(arquivo):
    lista_impressoras = win32print.EnumPrinters(2)
    
    impressora = lista_impressoras[5]
    win32print.SetDefaultPrinter(impressora[2])
    
    
    
    win32api.ShellExecute(0, "print", 'os.pdf', None, arquivo, 0)

def enviar(request):
    numero_os = request.POST.get('envia')
    
    
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT nomecliente, problemadescrito, servicoexecutado, extra6, extra7, valorprodutos, valorservicos, cnpjcpfcliente, extra12 FROM ordemservico WHERE (codigo = %i)" % (int(numero_os)))
    data = cursor.fetchall()
    cursor.close()
    for i in data:
        nome_cliente = i[0]
        problema_descrito = i[1]
        servico_executado = i[2]
        data_inicio = i[3]
        data_fim = i[4]
        valor_produtos = i[5]
        valor_servicos = i[6]
        cnpjcpf = i[7]
        assinado_por = i[8]
    
    
    system_state = 'dev'
    caminho_padrao = {'caminho': Caminhos_arquivos.objects.filter(nome = system_state).values()}
    for i in caminho_padrao['caminho']:
        consulta_caminho = i['caminho_os']
        consulta_caminho_logonit = i['caminhopadrao']
        consulta_caminho_assinaturas = i['assinaturas']
    print(consulta_caminho)
    consulta_caminho_logonit += 'logonit.jpg'

    
    
    
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT razaosocial, email FROM entidade WHERE cnpjcpf = '%s'" %(cnpjcpf))
    consulta_entidade = cursor.fetchall()
    cursor.close()   
    for x in consulta_entidade:
        email = x[1]
    confeccionar_os_pdf(numero_os, nome_cliente, problema_descrito, servico_executado, data_inicio, data_fim, 
                        valor_produtos, valor_servicos, email, assinado_por, consulta_caminho_logonit, consulta_caminho_assinaturas)
    # confeccionar_os_pdf(numero_os, nome_cliente, problema_descrito, servico_executado, data_inicio, data_fim, valor_produtos, valor_servicos, email, assinado_por)
    
    # cursor = connections['unico'].cursor()
    # cursor.execute("SELECT nomecliente, problemadescrito, servicoexecutado, extra6, extra7, valorprodutos, valorservicos, cnpjcpfcliente FROM ordemservico WHERE (codigo = %i)" % (int(numero_os)))
    # data = cursor.fetchall()
    # cursor.close()
    # for i in data:
    #     nome_cliente = i[0]
    #     problema_descrito = i[1]
    #     servico_executado = i[2]
    #     data_inicio = i[3]
    #     data_fim = i[4]
    #     valor_produtos = i[5]
    #     valor_servicos = i[6]
    #     cnpj = i[7]
        
    # print(cnpj)
    
    # cursor = connections['unico'].cursor()
    # cursor.execute("SELECT nome, email id FROM entidade WHERE cnpjcpf = '%s'" %(cnpj))
    # entidades = cursor.fetchall()
    # cursor.close()
    
    # for i in entidades:
    #     email = i[1]
    # print(email)
    
    
    # confeccionar_os_pdf(numero_os, nome_cliente, problema_descrito, servico_executado, data_inicio, data_fim, valor_produtos, valor_servicos, email, assinado_por)
    
    # confeccionar_os_pdf(numero_os, nome_cliente, problema_descrito, servico_executado, data_inicio, data_fim, valor_produtos, valor_servicos)
    envia_email(email, consulta_caminho)
    
    return render(request, 'os/enviar_email.html')
def envia_email(destinatario, consulta_caminho):
    import os
    import smtplib
    from email.message import EmailMessage
    email = 'contato@nit10.com.br'

    # with open('senha.txt') as f:
    #     senha = f.readlines()
        
    #     f.close()
        
    senha_do_email = 'Nit2987'

    # arquivo_imprimir = 'C:\\Users\\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\os.pdf'

    msg = EmailMessage()
    msg['Subject']  = 'Ordem de Serviço NIT10'
    msg['From'] = 'contato@nit10.com.br'
    msg['To'] = destinatario
    msg.set_content("Olá, Segue OS de Atendimento!!!!")
    



    with open(consulta_caminho, 'rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content, maintype='application', subtype='pdf', filename='os.pdf')

    with smtplib.SMTP_SSL('webmail.nit10.com.br', 465) as smtp:
        
        smtp.login(email, senha_do_email)
        smtp.send_message(msg)
    return()

@login_required(login_url='login')
@has_role_decorator('clientes')
def clientes_ordens(request):
    
    teste = (request.user.first_name).upper()
    nome = 'HOTEL LOCANDA LTDA'
    print(teste)
    
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT  cnpjcpf, nome, razaosocial, id FROM entidade WHERE nome = '%s'" %(nome))
    consulta_entidade = cursor.fetchall()
    cursor.close()
    
    
    for i in consulta_entidade:
        cnpj_entidade = i[0]
        
    print(cnpj_entidade)
    
    
    lista_os = {}
    
    
    # u = request.user.username
    # u = request.user.group
    # print(u)
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT codigo, nomecliente, problemadescrito FROM ordemservico WHERE (cnpjcpfcliente = '%s') AND (status = 1) ORDER BY codigo DESC" %(cnpj_entidade)) 
    os_aberta = cursor.fetchall()
    cursor.close()
    total_ordem_aberta = str(len(os_aberta))
    lista_os.update({'os_aberta' : total_ordem_aberta})
    
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT codigo, nomecliente, problemadescrito FROM ordemservico WHERE (cnpjcpfcliente = '%s') AND (status = 2) ORDER BY codigo DESC" %(cnpj_entidade)) 
    os_fin = cursor.fetchall()
    cursor.close()
    total_ordem_exec = str(len(os_fin))
    print(total_ordem_exec)
    lista_os.update({'os_exec' : total_ordem_exec})
   
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT codigo, nomecliente, problemadescrito FROM ordemservico WHERE (cnpjcpfcliente = '%s') AND (status = 3) ORDER BY codigo DESC" %(cnpj_entidade)) 
    os_fin = cursor.fetchall()
    cursor.close()
    total_ordem_fin = str(len(os_fin))
    print(total_ordem_exec)
    lista_os.update({'os_fin' : total_ordem_fin})
    # assign_role(request.user, 'clientes')
    return render(request, 'os/clientes_ordens.html', lista_os)





@login_required(login_url='login')
@has_role_decorator('clientes')
def cliente_visualiza_os(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        print(status)
    
        return render(request, 'os/clientes_visualiza_ordens.html')
    
    
    
@login_required(login_url='login')
def dashboard(request):
    cursor = connections['unico'].cursor()
    cursor.execute("SELECT codigo, nomecliente FROM ordemservico ORDER BY codigo DESC") 
    consulta_os = cursor.fetchone()
    
    
    lista_consulta = [consulta_os]
    for i in lista_consulta:
        os = i[0]
    caminho_historico = 'C:\\Users\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\historico_os.txt' 
        
    caminho_nova_os = 'C:\\Users\ZeCar\\Documents\\projetos_python\\unico_web_60\\venv\\proj_unico_web\\nova_os.txt' 
    with open(caminho_nova_os, 'r') as arquivo:
        n_ordem_atual = int(arquivo.readline())
    
    dict_novas_os = {}
    consuta_geral = 10
    diferenca_entre_os = os - n_ordem_atual
    if n_ordem_atual == os:
        alarme = str(0)
        dict_novas_os.update({'alarme': alarme})
        consulta_os_completas = cursor.fetchmany(consuta_geral)
        dict_novas_os.update({'consulta_os': consulta_os_completas})
    else:
        alarme = str(1)
        
        print(diferenca_entre_os)
        if diferenca_entre_os != 0:
            dict_novas_os.update({'alarme': alarme})
            consulta_os_completas = cursor.fetchmany(diferenca_entre_os)
            dict_novas_os.update({'consulta_os': consulta_os_completas})
            
            with open(caminho_nova_os, 'w') as arquivo:
                arquivo.write(str(os))
                   
    
    
    cursor.close()
  
    return render(request, 'dashboards/dashboard.html', dict_novas_os)       

def sobre(request):
    pass
    return render(request, 'dashboards/sobre.html')


def incluir_veiculos(request):
    pass    
    return render(request, 'cadastros/incluir_veiculos.html')

def cadastrar_veiculos(request):
    if request.method == 'POST':

        novo_veiculo = Veiculos()
        novo_veiculo.modelo = request.POST.get('modelo').upper()
        novo_veiculo.placa = request.POST.get('placa').upper()
        novo_veiculo.save()
        
        
        
        return render(request, 'cadastros/cadastrar_veiculos.html')




def incluir_motoristas(request):
    pass    
    return render(request, 'cadastros/incluir_motoristas.html')

def cadastrar_motoristas(request):
    if request.method == 'POST':

        novo_veiculo = Motoristas()
        novo_veiculo.nome = request.POST.get('motorista').upper()
   
        novo_veiculo.save()
        
        
        
        return render(request, 'cadastros/cadastrar_motoristas.html')
    

def consulta_ordem_abastecimentos(request):
    consulta_ordem_abast = {'ordens' : Ordem_abastecimento.objects.all().values().order_by('-id')}
    return render(request, 'cadastros/consulta_ordem_abastecimentos.html', consulta_ordem_abast)

def altera_valor_ordem_abastecimento(request):
    if request.method == 'POST':
        num_ordem_abast = request.POST.get('subject')
        consulta_ordem_abast = {'ordens' : Ordem_abastecimento.objects.filter(numero=num_ordem_abast).values()}
        print(consulta_ordem_abast)
        
        return render(request, 'cadastros/altera_valor_ordem_abastecimento.html', consulta_ordem_abast)
    
def registra_valor_ordem_abastecimento(request):
    if request.method == 'POST':
        valor = request.POST.get('valor')
        ordem = request.POST.get('registra')
        print(valor)
        novo_valor = Ordem_abastecimento.objects.get(numero=ordem)
        novo_valor.valor = valor
        novo_valor.save()
        return render(request,'cadastros/registra_valor_ordem_abastecimento.html')