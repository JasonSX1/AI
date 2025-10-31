from nltk import word_tokenize, corpus
from inicializador_modelo import *
from transcritor import *
import secrets
import pyaudio
import wave
import os
import json
from lampada import *
from som import *
from threading import Thread
from flask import Flask, Response, request, send_from_directory, jsonify
# import pydub # Removido
import torch
import subprocess  # Adicionado para rodar o FFmpeg
import shutil      # Adicionado para checar se o FFmpeg existe

# Configurações principais
LINGUAGEM = "portuguese"
FORMATO = pyaudio.paInt16
CANAIS = 1
AMOSTRAS = 1024
TAXA_AMOSTRAGEM = 44100 # Manter esta taxa para a conversão FFmpeg
TEMPO_GRAVACAO = 5
CAMINHO_AUDIO_FALAS = r"C:\Users\Usuario\Desktop\IA\assistente virtual\temp"
CONFIGURACOES = r"C:\Users\Usuario\Desktop\IA\assistente virtual\config.json"

# Modos de funcionamento
MODO_LINHA_DE_COMANDO = 1
MODO_WEB = 2
MODO_DE_FUNCIONAMETO = MODO_WEB


def iniciar(dispositivo):
    modelo_iniciado, processador, modelo = iniciar_modelo(MODELOS[0], dispositivo)
    # Inicializar PyAudio mesmo se MODO_WEB for o alvo, para não quebrar a variável 'gravador'
    # mas ela será usada apenas no MODO_LINHA_DE_COMANDO.
    try:
        gravador = pyaudio.PyAudio()
    except Exception as e:
        print(f"Aviso: Não foi possível inicializar o pyaudio. O modo LINHA DE COMANDO não funcionará. Erro: {e}")
        gravador = None 
        
    palavras_de_parada = set(corpus.stopwords.words(LINGUAGEM))

    with open(CONFIGURACOES, "r", encoding="utf-8") as arquivo_configuracoes:
        configuracoes = json.load(arquivo_configuracoes)
        acoes = configuracoes.get("acoes", [])

    return modelo_iniciado, processador, modelo, gravador, palavras_de_parada, acoes


def iniciar_atuadores():
    atuadores = []
    if iniciar_lampada():
        atuadores.append({"nome": "lâmpada", "atuacao": atuar_sobre_lampada})
    if iniciar_som():
        atuadores.append({"nome": "Sistema de som", "atuacao": atuar_sobre_som})
    return atuadores


def capturar_fala(gravador):
    if not gravador:
        raise Exception("Gravador PyAudio não inicializado.")

    gravacao = gravador.open(format=FORMATO, channels=CANAIS, rate=TAXA_AMOSTRAGEM,
                             input=True, frames_per_buffer=AMOSTRAS)

    print("Fale alguma coisa...")

    fala = []
    for _ in range(0, int(TAXA_AMOSTRAGEM / AMOSTRAS * TEMPO_GRAVACAO)):
        fala.append(gravacao.read(AMOSTRAS))

    gravacao.stop_stream()
    gravacao.close()
    print("Fala capturada.")
    return fala


def gravar_fala(gravador, fala):
    if not gravador:
        return False, None
        
    gravado, arquivo = False, os.path.join(CAMINHO_AUDIO_FALAS, f"{secrets.token_hex(16)}.wav")

    try:
        wav = wave.open(arquivo, "wb")
        wav.setnchannels(CANAIS)
        wav.setsampwidth(gravador.get_sample_size(FORMATO))
        wav.setframerate(TAXA_AMOSTRAGEM)
        wav.writeframes(b"".join(fala))
        wav.close()
        gravado = True
    except Exception as e:
        print(f"Erro ao gravar fala: {e}")

    return gravado, arquivo


def processar_transcricao(transcricao, palavras_de_parada):
    tokens = word_tokenize(transcricao.lower())
    return [t for t in tokens if t not in palavras_de_parada]


def validar_comando(comando, acoes):
    if len(comando) < 2:
        return False, None, None

    acao, dispositivo = comando[0], comando[1]
    for acao_prevista in acoes:
        if acao == acao_prevista["nome"] and dispositivo in acao_prevista["dispositivos"]:
            return True, acao, dispositivo
    return False, None, None


def atuar(acao, dispositivo, atuadores):
    for atuador in atuadores:
        print(f"Enviando comando para {atuador['nome']}...")
        Thread(target=atuador["atuacao"], args=[acao, dispositivo]).start()


##########################
# MODO LINHA DE COMANDO
##########################
def ativar_linha_de_comando():
    # Aviso: Este modo ainda requer PyAudio, PyWave e todas as suas dependências.
    if not gravador:
        print("Modo Linha de Comando não pode ser ativado: PyAudio não inicializado.")
        return

    while True:
        try:
            fala = capturar_fala(gravador)
            gravado, arquivo = gravar_fala(gravador, fala)
            if not gravado:
                print("Erro ao gravar fala.")
                continue

            fala = carregar_fala(arquivo)
            transcricao = transcrever_fala(dispositivo, fala, modelo, processador)

            if os.path.exists(arquivo):
                os.remove(arquivo)

            comando = processar_transcricao(transcricao, palavras_de_parada)
            print(f"Comando: {comando}")

            valido, acao, dispositivo_alvo = validar_comando(comando, acoes)
            if valido:
                print(f"Executando {acao} sobre {dispositivo_alvo}")
                atuar(acao, dispositivo_alvo, atuadores)
            else:
                print("Comando inválido.")
        except Exception as e:
            print(f"Erro no modo linha de comando: {e}")


##########################
# MODO WEB (FLASK)
##########################
servico = Flask(__name__, static_folder="public")


@servico.route("/")
def acessar_pagina():
    return send_from_directory("public", "index.html")


@servico.route("/<path:path>")
def acessar_pasta_estatica(path):
    return send_from_directory("public", path)


@servico.post("/reconhecer_comando")
def reconhecer_comando():
    if "audio" not in request.files:
        return Response("Arquivo de áudio não encontrado", status=400)

    audio = request.files["audio"]
    # 1. SALVAR O ARQUIVO WEB-M ENVIADO
    # O frontend envia WebM, salvamos como .webm
    caminho_webm = os.path.join(CAMINHO_AUDIO_FALAS, f"{secrets.token_hex(16)}.webm")
    # Define o caminho de saída para o WAV que o modelo espera
    caminho_wav = os.path.join(CAMINHO_AUDIO_FALAS, f"{secrets.token_hex(16)}.wav")
    
    audio.save(caminho_webm)

    # Verifica se o FFmpeg está disponível
    if shutil.which("ffmpeg") is None:
        mensagem_erro = "FFmpeg não encontrado no PATH. Necessário para conversão de WebM para WAV."
        print(f"Erro: {mensagem_erro}")
        # Limpa o arquivo .webm
        if os.path.exists(caminho_webm):
            os.remove(caminho_webm)
        return jsonify({"erro": mensagem_erro}), 500

    # 2. CONVERTER WEB-M PARA WAV USANDO FFmpeg
    try:
        # Comando do FFmpeg: -i (input), -ac 1 (Mono), -ar (Taxa de Amostragem), -f wav (Forçar WAV)
        subprocess.run(
            [
                "ffmpeg", 
                "-i", caminho_webm, 
                "-ac", "1",                                  # Mono (1 canal)
                "-ar", str(servico.config["taxa_amostragem"]), # Taxa de amostragem
                "-f", "wav",                                 # Força o formato WAV
                caminho_wav
            ],
            check=True,  # Levanta erro se o FFmpeg falhar
            capture_output=True,
            text=True
        )
        
    except subprocess.CalledProcessError as e:
        print(f"Erro na conversão FFmpeg: {e.stderr}")
        # Limpa ambos os arquivos em caso de falha de conversão
        if os.path.exists(caminho_webm):
            os.remove(caminho_webm)
        if os.path.exists(caminho_wav):
            os.remove(caminho_wav)
        return jsonify({"erro": f"Falha na conversão de áudio (FFmpeg): {e.stderr}"}), 500
    
    # 3. PROCESSAR A FALA CONVERTIDA (WAV)
    try:
        transcricao = transcrever_fala(
            servico.config["dispositivo"],
            carregar_fala(caminho_wav),
            servico.config["modelo"],
            servico.config["processador"]
        )

        comando = processar_transcricao(transcricao, servico.config["palavras_de_parada"])
        valido, acao, dispositivo_alvo = validar_comando(comando, servico.config["acoes"])

        if valido:
            atuar(acao, dispositivo_alvo, servico.config["atuadores"])
            return jsonify({"transcricao": transcricao, "status": "comando executado"}), 200
        else:
            return jsonify({"transcricao": transcricao, "status": "comando não reconhecido"}), 200

    except Exception as e:
        print(f"Erro ao processar fala: {str(e)}")
        return jsonify({"erro": str(e)}), 500

    finally:
        # 4. LIMPAR ARQUIVOS TEMPORÁRIOS
        # Remove o arquivo webm original
        if os.path.exists(caminho_webm):
            os.remove(caminho_webm)
        # Remove o arquivo wav convertido
        if os.path.exists(caminho_wav):
            os.remove(caminho_wav)


def ativar_web(dispositivo, modelo, processador, palavras_de_parada, acoes, atuadores):
    # Adiciona a taxa de amostragem às configurações do serviço para uso no FFmpeg
    servico.config.update({
        "dispositivo": dispositivo,
        "modelo": modelo,
        "processador": processador,
        "palavras_de_parada": palavras_de_parada,
        "acoes": acoes,
        "atuadores": atuadores,
        "taxa_amostragem": TAXA_AMOSTRAGEM # Adicionado
    })
    print("Iniciando modo WEB...")
    servico.run(host="0.0.0.0", port=5000, debug=False)


##########################
# MAIN
##########################
if __name__ == "__main__":
    # Verifica se a pasta temporária existe e a cria se necessário
    if not os.path.exists(CAMINHO_AUDIO_FALAS):
        os.makedirs(CAMINHO_AUDIO_FALAS)
        
    dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"

    iniciado, processador, modelo, gravador, palavras_de_parada, acoes = iniciar(dispositivo)

    if iniciado:
        atuadores = iniciar_atuadores()
        if MODO_DE_FUNCIONAMETO == MODO_LINHA_DE_COMANDO:
            ativar_linha_de_comando()
        elif MODO_DE_FUNCIONAMETO == MODO_WEB:
            ativar_web(dispositivo, modelo, processador, palavras_de_parada, acoes, atuadores)
        else:
            print("Modo de funcionamento não implementado.")
    else:
        print("Erro de inicialização.")