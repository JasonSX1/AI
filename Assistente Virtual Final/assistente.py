from flask import Flask, Response, request, send_from_directory
from nltk import word_tokenize, corpus
from inicializador_modelo import *
from threading import Thread
from transcritor import *
from datetime import datetime
from fuzzy_match import *
import secrets
import pyaudio
import wave
import json
import os
import random
import torch

from atuadoress.fonte_bancada import *
from atuadoress.estacao_solda import *
from atuadoress.monitor_energia import *
from atuadoress.sensor_temperatura import *
from atuadoress.registro_tarefas import *

LINGUAGEM = "portuguese"
FORMATO = pyaudio.paInt16
CANAIS = 1
AMOSTRAS = 1024
TEMPO_GRAVACAO = 5
CAMINHO_AUDIO_FALAS = r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\temp"
CONFIGURACOES = r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\config.json"

MODO_LINHA_DE_COMANDO = 1
MODO_WEB = 2
MODO_DE_FUNCIONAMENTO = MODO_WEB # MODO_LINHA_DE_COMANDO

def iniciar(dispositivo):
    modelo_iniciado, processador, modelo = iniciar_modelo(MODELOS[0], dispositivo)
    gravador = pyaudio.PyAudio()
    palavras_de_parada = set(corpus.stopwords.words(LINGUAGEM))

    with open(CONFIGURACOES, "r", encoding="utf-8") as arquivo_configuracoes:
        configuracoes = json.load(arquivo_configuracoes)
        acoes = configuracoes["acoes"]
        arquivo_configuracoes.close()

    return modelo_iniciado, processador, modelo, gravador, palavras_de_parada, acoes

def iniciar_atuadores():
    """Inicializa todos os atuadores da bancada eletrônica"""
    atuadores = []
    if iniciar_fonte_bancada():
        atuadores.append({"nome": "fonte de bancada", "atuacao": atuar_sobre_fonte_bancada})
    if iniciar_estacao_solda():
        atuadores.append({"nome": "estação de solda", "atuacao": atuar_sobre_estacao_solda})
    if iniciar_monitor_energia():
        atuadores.append({"nome": "monitor de energia", "atuacao": atuar_sobre_monitor_energia})
    if iniciar_sensor_temperatura():
        atuadores.append({"nome": "sensor de temperatura", "atuacao": atuar_sobre_sensor_temperatura})
    if iniciar_registro_tarefas():
        atuadores.append({"nome": "sistema de registro", "atuacao": atuar_sobre_registro_tarefas})
    return atuadores

def capturar_fala(gravador):
    gravacao = gravador.open(format=FORMATO, channels=CANAIS, rate=TAXA_AMOSTRAGEM, input=True, frames_per_buffer=AMOSTRAS)
    print("fale alguma coisa...")
    fala = []
    for _ in range(0, int(TAXA_AMOSTRAGEM/AMOSTRAS*TEMPO_GRAVACAO)):
        fala.append(gravacao.read(AMOSTRAS))
    gravacao.stop_stream()
    gravacao.close()
    print("fala capturada")
    return fala

def gravar_fala(gravador, fala):
    gravado, arquivo = False, f"{CAMINHO_AUDIO_FALAS}/{secrets.token_hex(32).lower()}.wav"
    try:
        wav = wave.open(arquivo, "wb")
        wav.setnchannels(CANAIS)
        wav.setsampwidth(gravador.get_sample_size(FORMATO))
        wav.setframerate(TAXA_AMOSTRAGEM)
        wav.writeframes(b"".join(fala))
        wav.close()
        gravado = True
    except Exception as e:
        print(f"erro gravando arquivo de fala: {str(e)}")
    return gravado, arquivo

def processar_transcricao(transcricao, palavras_de_parada):
    comando = []
    tokens = word_tokenize(transcricao)
    for token in tokens:
        if token not in palavras_de_parada:
            comando.append(token)
    return comando

def validar_comando(comando, acoes):
    valido, acao, dispositivo = False, None, None
    comando_str = " ".join(comando)

    # --- LÓGICA MELHORADA PARA REGISTRO DE TAREFA ---
    acoes_registro = ["registrar tarefa", "anotar tarefa", "salvar tarefa", "iniciar tarefa", "nova tarefa", "iniciar reparo", "novo reparo"]
    for gatilho in acoes_registro:
        if gatilho in comando_str:
            valido = True
            acao = "registrar" # Padroniza a ação
            dispositivo = "tarefa" # Padroniza o dispositivo
            print(f"[REGISTRO] Comando de registro detectado.")
            return valido, acao, dispositivo
    # --- FIM DA LÓGICA MELHORADA ---

    if len(comando) >= 2:
        acao = comando[0]
        dispositivo = " ".join(comando[1:]) # Permite dispositivos com mais de uma palavra

        # Tenta match exato primeiro
        for acao_prevista in acoes:
            if acao == acao_prevista["nome"]:
                if dispositivo in acao_prevista["dispositivos"]:
                    valido = True
                    break
        
        # Se não encontrou match exato, tenta fuzzy matching
        if not valido:
            acao_corrigida = corrigir_acao(acao, acoes)
            if acao_corrigida:
                acao = acao_corrigida
                for acao_prevista in acoes:
                    if acao == acao_prevista["nome"]:
                        dispositivo_corrigido = corrigir_dispositivo(dispositivo, acao_prevista["dispositivos"])
                        if dispositivo_corrigido:
                            dispositivo = dispositivo_corrigido
                            valido = True
                            print(f"[FUZZY] Comando corrigido: {acao} {dispositivo}")
                            break
    return valido, acao, dispositivo

def atuar(acao, dispositivo, atuadores):
    """Executa atuação e retorna resultados"""
    
    # --- MUDANÇA AQUI ---
    # Se for comando de registro, não faz nada aqui. O JS/outro endpoint cuidará disso.
    if acao == "registrar" and dispositivo == "tarefa":
        print("Ativação do modo de registro via JS")
        return [{"sucesso": True, "mensagem": "Modo de registro ativado. Digite a tarefa."}]
    
    resultados = []
    for atuador in atuadores:
        print(f"enviando comando para {atuador['nome']}")
        # Evita que o atuador de registro seja chamado com comandos normais
        if atuador["nome"] == "sistema de registro":
            continue
            
        resultado = atuador["atuacao"](acao, dispositivo)
        if resultado:
            resultados.append(resultado)
    return resultados

############################## linha de comando
# (sem alterações)
##############################

############################## servico web

servico = Flask("assistente", static_folder="front")

@servico.get("/")
def acessar_pagina():
    return send_from_directory("front", "index.html")

@servico.get("/<path:caminho>")
def acessar_pasta_estatica(caminho):
    return send_from_directory("front", caminho)

@servico.get("/estado")
def obter_estado():
    """Retorna o estado atual de todos os equipamentos"""
    from atuadoress.fonte_bancada import obter_estado_fonte
    from atuadoress.estacao_solda import obter_estado_estacao
    # from sensor_temperatura import obter_temperatura_ambiente # <-- REMOVA/COMENTE ISSO

    fonte = obter_estado_fonte()
    estacao = obter_estado_estacao()

    # --- CORREÇÃO AQUI ---
    # Temperatura ambiente simulada (como estava antes)
    temp_ambiente = random.randint(22, 28) 

    estado = {
        "fonte": fonte,
        "estacao": estacao,
        "temperatura_ambiente": temp_ambiente, # Retorna a temperatura simulada
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return Response(json.dumps(estado, ensure_ascii=False), status=200, mimetype='application/json; charset=utf-8')

@servico.post("/reconhecer_comando")
def reconhecer_comando():
    if "fala" not in request.files:
        return Response(status=400)
    
    fala = request.files["fala"]
    caminho_arquivo = f"{CAMINHO_AUDIO_FALAS}/{secrets.token_hex(32).lower()}.wav"
    fala.save(caminho_arquivo)

    try:
        transcricao = transcrever_fala(servico.config["dispositivo"], carregar_fala(caminho_arquivo), servico.config["modelo"], servico.config["processador"])
        comando = processar_transcricao(transcricao, servico.config["palavras_de_parada"])
        valido, acao, dispositivo_alvo = validar_comando(comando, servico.config["acoes"])

        if valido:
            print(f"comando válido, executar atuação")
            resultados = atuar(acao, dispositivo_alvo, servico.config["atuadores"])
            
            mensagens = []
            for resultado in resultados:
                if resultado and "mensagem" in resultado:
                    mensagens.append(resultado["mensagem"])
            
            # --- MUDANÇA AQUI ---
            # Verifica se é comando de registro de tarefa
            is_registro = (acao == "registrar" and dispositivo_alvo == "tarefa")
            
            resposta = {
                "transcricao": transcricao,
                "acao": acao,
                "dispositivo": dispositivo_alvo,
                "sucesso": True,
                "mensagens": mensagens,
                "resultados": resultados,
                "modo_registro": is_registro  # <-- Este flag dirá ao JS para abrir o painel de texto
            }
            return Response(json.dumps(resposta, ensure_ascii=False), status=200, mimetype='application/json; charset=utf-8')
        else:
            return Response(json.dumps({
                "transcricao": transcricao,
                "sucesso": False,
                "mensagens": ["⚠️ Comando não reconhecido"]
            }, ensure_ascii=False), status=200, mimetype='application/json; charset=utf-8')
    except Exception as e:
        print(f"erro ao processar fala: {str(e)}")
        return Response(json.dumps({"sucesso": False, "mensagens": [f"❌ Erro ao processar: {str(e)}"]}), status=500, mimetype='application/json; charset=utf-8')
    finally:
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

# --- NOVO ENDPOINT ---
@servico.post("/salvar_tarefa_texto")
def salvar_tarefa_texto():
    """Endpoint que recebe um JSON com o texto da tarefa e o salva."""
    data = request.get_json()
    if not data or 'tarefa' not in data:
        return Response(json.dumps({"sucesso": False, "mensagens": ["Nenhum texto de tarefa recebido."]}), status=400, mimetype='application/json; charset=utf-8')
    
    texto_tarefa = data['tarefa']
    print(f"[REGISTRO] Recebido texto para salvar: {texto_tarefa}")
    
    try:
        from atuadoress.registro_tarefas import atuar_sobre_registro_tarefas
        # Chama a função de registro com a ação "registrar" e o texto como "dispositivo"
        resultado = atuar_sobre_registro_tarefas("registrar", texto_tarefa) 
        
        if resultado and resultado.get("sucesso"):
            return Response(json.dumps({"sucesso": True, "mensagens": [resultado.get("mensagem", "Tarefa salva!")]}), status=200, mimetype='application/json; charset=utf-8')
        else:
            return Response(json.dumps({"sucesso": False, "mensagens": [resultado.get("mensagem", "Erro ao salvar no backend.")]}), status=500, mimetype='application/json; charset=utf-8')
    except Exception as e:
        print(f"erro ao salvar tarefa: {str(e)}")
        return Response(json.dumps({"sucesso": False, "mensagens": [f"Erro interno no servidor: {str(e)}"]}), status=500, mimetype='application/json; charset=utf-8')
# --- FIM DO NOVO ENDPOINT ---

def ativar_web(dispositivo, modelo, processador, palavras_de_parada, acoes, atuadores):
    servico.config["dispositivo"] = dispositivo
    servico.config["modelo"] = modelo
    servico.config["processador"] = processador
    servico.config["palavras_de_parada"] = palavras_de_parada
    servico.config["acoes"] = acoes
    servico.config["atuadores"] = atuadores
    servico.run(host="0.0.0.0", port=7001)

if __name__ == "__main__":
    dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"
    iniciado, processador, modelo, gravador, palavras_de_parada, acoes = iniciar(dispositivo)
    if iniciado:
        atuadores = iniciar_atuadores()
        if MODO_DE_FUNCIONAMENTO == MODO_LINHA_DE_COMANDO:
            ativar_linha_de_comando()
        elif MODO_DE_FUNCIONAMENTO == MODO_WEB:
            ativar_web(dispositivo, modelo, processador, palavras_de_parada, acoes, atuadores)
        else:
            print("modo de funcionamento não implementado")
    else:
        print("ocorre um erro de inicialização")