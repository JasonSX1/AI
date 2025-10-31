from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import soundfile as sf
import torch
import numpy as np

MODELO = "lgris/wav2vec2-large-xlsr-open-brazilian-portuguese-v2"

AUDIOS = [
    {
        "comando": "ligar fonte de bancada",
        "wav": r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\audios\ligar_fonte.wav"
    },
    {
        "comando": "desligar fonte de bancada",
        "wav": r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\audios\desligar_fonte.wav"
    },
    {
        "comando": "ligar estação de solda",
        "wav": r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\audios\ligar_solda.wav"
    },
    {
        "comando": "desligar estação de solda",
        "wav": r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\audios\desligar_solda.wav"
    },
    {
        "comando": "monitorar energia consumida",
        "wav": r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\audios\monitorar_energia.wav"
    },
    {
        "comando": "verificar temperatura dos equipamentos",
        "wav": r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\audios\verificar_temperatura.wav"
    },
    {
        "comando": "registrar nova tarefa de reparo",
        "wav": r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\audios\registrar_tarefa.wav"
    }
]

def iniciar_modelo(nome_modelo, dispositivo="cpu"):
    iniciado, processador, modelo = False, None, None

    try:
        processador = Wav2Vec2Processor.from_pretrained(nome_modelo)
        modelo = Wav2Vec2ForCTC.from_pretrained(nome_modelo).to(dispositivo)

        iniciado = True
    except Exception as e:
        print(f"erro iniciando o modelo: {str(e)}")

    return iniciado, processador, modelo

TAXA_AMOSTRAGEM = 16_000

def carregar_fala(caminho_audio):
    """Carrega arquivo de áudio usando soundfile (mais compatível)"""
    # Carrega o áudio com soundfile
    audio, amostragem = sf.read(caminho_audio, dtype='float32')
    
    # Converte para tensor
    audio = torch.from_numpy(audio)
    
    # Se for estéreo, converte para mono
    if len(audio.shape) > 1:
        audio = torch.mean(audio, dim=1)
    
    # Reamostrar se necessário
    if amostragem != TAXA_AMOSTRAGEM:
        # Cálculo simples de reamostragem
        duracao = len(audio) / amostragem
        novo_tamanho = int(duracao * TAXA_AMOSTRAGEM)
        indices = torch.linspace(0, len(audio) - 1, novo_tamanho)
        audio = torch.nn.functional.interpolate(
            audio.unsqueeze(0).unsqueeze(0),
            size=novo_tamanho,
            mode='linear',
            align_corners=True
        ).squeeze()
    
    return audio

def transcrever_fala(dispositivo, fala, modelo, processador):
    entrada = processador(fala, return_tensors="pt", sampling_rate=TAXA_AMOSTRAGEM).input_values.to(dispositivo)
    saida = modelo(entrada).logits

    predicao = torch.argmax(saida, dim=-1)
    transcricao = processador.batch_decode(predicao)[0]

    return transcricao.lower()

if __name__ == "__main__":
    dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"

    iniciado, processador, modelo = iniciar_modelo(MODELO, dispositivo)
    if iniciado:
        for audio in AUDIOS:
            print(f"testando transcrição do comando: {audio['comando']}")

            fala = carregar_fala(audio["wav"])
            transcricao = transcrever_fala(dispositivo, fala, modelo, processador)

            print(f"transcrição: {transcricao}")