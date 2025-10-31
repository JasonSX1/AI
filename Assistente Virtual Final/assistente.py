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

from fonte_bancada import *
from estacao_solda import *
from monitor_energia import *
from sensor_temperatura import *
from registro_tarefas import *

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
        atuadores.append({
            "nome": "fonte de bancada",
            "atuacao": atuar_sobre_fonte_bancada
        })

    if iniciar_estacao_solda():
        atuadores.append({
            "nome": "estação de solda",
            "atuacao": atuar_sobre_estacao_solda
        })

    if iniciar_monitor_energia():
        atuadores.append({
            "nome": "monitor de energia",
            "atuacao": atuar_sobre_monitor_energia
        })

    if iniciar_sensor_temperatura():
        atuadores.append({
            "nome": "sensor de temperatura",
            "atuacao": atuar_sobre_sensor_temperatura
        })

    if iniciar_registro_tarefas():
        atuadores.append({
            "nome": "sistema de registro",
            "atuacao": atuar_sobre_registro_tarefas
        })

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

    if len(comando) >= 2:
        acao = comando[0]
        dispositivo = comando[1]

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
    resultados = []
    
    for atuador in atuadores:
        print(f"enviando comando para {atuador['nome']}")
        resultado = atuador["atuacao"](acao, dispositivo)
        if resultado:
            resultados.append(resultado)
    
    return resultados

############################## linha de comando

def ativar_linha_de_comando():
    while True:
        fala = capturar_fala(gravador)
        gravado, arquivo = gravar_fala(gravador, fala)
        if gravado:
            fala = carregar_fala(arquivo)
            transcricao = transcrever_fala(dispositivo, fala, modelo, processador)

            if os.path.exists(arquivo):
                os.remove(arquivo)

            comando = processar_transcricao(transcricao, palavras_de_parada)
            print(f"comando: {comando}")

            valido, acao, dispositivo_alvo = validar_comando(comando, acoes)
            if valido:
                print(f"executando {acao} sobre {dispositivo_alvo}")

                atuar(acao, dispositivo_alvo, atuadores)
            else:
                print("comando inválido")
        else:
            print("ocorreu um erro gravando a fala")

############################## servico web

servico = Flask("assistente", static_folder="public")

@servico.get("/")
def acessar_pagina():
    return send_from_directory("public", "index.html")

@servico.get("/<path:caminho>")
def acessar_pasta_estatica(caminho):
    return send_from_directory("public", caminho)

@servico.get("/estado")
def obter_estado():
    """Retorna o estado atual de todos os equipamentos"""
    from fonte_bancada import obter_estado_fonte
    from estacao_solda import obter_estado_estacao
    import random
    
    fonte = obter_estado_fonte()
    estacao = obter_estado_estacao()
    
    # Temperatura ambiente simulada
    temp_ambiente = random.randint(22, 28)
    
    estado = {
        "fonte": fonte,
        "estacao": estacao,
        "temperatura_ambiente": temp_ambiente,
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
            
            # Coleta mensagens dos resultados
            mensagens = []
            for resultado in resultados:
                if resultado and "mensagem" in resultado:
                    mensagens.append(resultado["mensagem"])
            
            resposta = {
                "transcricao": transcricao,
                "acao": acao,
                "dispositivo": dispositivo_alvo,
                "sucesso": True,
                "mensagens": mensagens,
                "resultados": resultados
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

        return Response(json.dumps({
            "sucesso": False,
            "mensagens": [f"❌ Erro ao processar: {str(e)}"]
        }, ensure_ascii=False), status=500, mimetype='application/json; charset=utf-8')
    finally:
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

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