"""
Script auxiliar para gravar os áudios de teste
Execute este script para gravar os 7 comandos necessários para os testes
"""
import pyaudio
import wave
import os

# Configurações
FORMATO = pyaudio.paInt16
CANAIS = 1
TAXA_AMOSTRAGEM = 16000
AMOSTRAS = 1024
TEMPO_GRAVACAO = 3  # segundos
CAMINHO_AUDIOS = r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\audios"

# Lista de comandos a serem gravados
COMANDOS = [
    {
        "nome": "ligar_fonte.wav",
        "texto": "Ligar fonte de bancada"
    },
    {
        "nome": "desligar_fonte.wav",
        "texto": "Desligar fonte de bancada"
    },
    {
        "nome": "ligar_solda.wav",
        "texto": "Ligar estação de solda"
    },
    {
        "nome": "desligar_solda.wav",
        "texto": "Desligar estação de solda"
    },
    {
        "nome": "monitorar_energia.wav",
        "texto": "Monitorar energia consumida"
    },
    {
        "nome": "verificar_temperatura.wav",
        "texto": "Verificar temperatura dos equipamentos"
    },
    {
        "nome": "registrar_tarefa.wav",
        "texto": "Registrar nova tarefa de reparo"
    }
]

def gravar_audio(arquivo, comando_texto):
    """Grava um áudio do microfone"""
    gravador = pyaudio.PyAudio()
    
    print(f"\n{'='*60}")
    print(f"Prepare-se para falar: '{comando_texto}'")
    print(f"{'='*60}")
    input("Pressione ENTER quando estiver pronto...")
    
    print(f"\n🎤 GRAVANDO... Fale agora: '{comando_texto}'")
    
    stream = gravador.open(
        format=FORMATO,
        channels=CANAIS,
        rate=TAXA_AMOSTRAGEM,
        input=True,
        frames_per_buffer=AMOSTRAS
    )
    
    frames = []
    for _ in range(0, int(TAXA_AMOSTRAGEM / AMOSTRAS * TEMPO_GRAVACAO)):
        data = stream.read(AMOSTRAS)
        frames.append(data)
    
    print("✓ Gravação concluída!")
    
    stream.stop_stream()
    stream.close()
    
    # Salva o arquivo
    caminho_completo = os.path.join(CAMINHO_AUDIOS, arquivo)
    wf = wave.open(caminho_completo, 'wb')
    wf.setnchannels(CANAIS)
    wf.setsampwidth(gravador.get_sample_size(FORMATO))
    wf.setframerate(TAXA_AMOSTRAGEM)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    gravador.terminate()
    
    print(f"✓ Arquivo salvo: {caminho_completo}")
    
    # Pergunta se quer regravar
    resposta = input("\nDeseja regravar este comando? (s/n): ").lower()
    if resposta == 's':
        print("Regravando...")
        gravar_audio(arquivo, comando_texto)

def main():
    print("\n" + "="*60)
    print("GRAVADOR DE ÁUDIOS PARA TESTES DO ASSISTENTE")
    print("="*60)
    print("\nEste script irá gravar os 7 comandos de voz necessários")
    print("para os testes automatizados do assistente virtual.\n")
    print("INSTRUÇÕES:")
    print("1. Certifique-se de estar em um ambiente silencioso")
    print("2. Fale de forma clara e natural")
    print("3. Você terá 3 segundos para falar cada comando")
    print("4. Você poderá regravar se não gostar do resultado")
    print("="*60)
    
    # Cria diretório se não existir
    if not os.path.exists(CAMINHO_AUDIOS):
        os.makedirs(CAMINHO_AUDIOS)
        print(f"\n✓ Diretório criado: {CAMINHO_AUDIOS}")
    
    input("\nPressione ENTER para começar...")
    
    # Grava cada comando
    for i, comando in enumerate(COMANDOS, 1):
        print(f"\n\n{'#'*60}")
        print(f"COMANDO {i} DE {len(COMANDOS)}")
        print(f"{'#'*60}")
        gravar_audio(comando["nome"], comando["texto"])
    
    print("\n" + "="*60)
    print("✓ TODOS OS ÁUDIOS FORAM GRAVADOS COM SUCESSO!")
    print("="*60)
    print(f"\nArquivos salvos em: {CAMINHO_AUDIOS}")
    print("\nAgora você pode executar os testes com:")
    print("  python test_assistente.py")
    print("\nOu executar o assistente com:")
    print("  python assistente.py")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
