"""
Script de teste rápido para verificar se tudo está funcionando
"""
import sys

print("="*70)
print("TESTE RÁPIDO - ASSISTENTE VIRTUAL")
print("="*70)

# Teste 1: Imports básicos
print("\n[1/7] Testando imports básicos...")
try:
    import torch
    import soundfile
    import transformers
    import nltk
    import pyaudio
    import flask
    print("  ✅ Todos os imports básicos OK")
except Exception as e:
    print(f"  ❌ Erro nos imports: {e}")
    sys.exit(1)

# Teste 2: NLTK data
print("\n[2/7] Testando recursos NLTK...")
try:
    from nltk import corpus
    palavras = corpus.stopwords.words("portuguese")
    print(f"  ✅ NLTK OK - {len(palavras)} stopwords carregadas")
except Exception as e:
    print(f"  ❌ Erro no NLTK: {e}")
    print("  Execute: python inicializador_nltk.py")
    sys.exit(1)

# Teste 3: Soundfile para áudio
print("\n[3/7] Testando soundfile...")
try:
    import soundfile as sf
    print("  ✅ Soundfile OK")
except Exception as e:
    print(f"  ❌ Erro no soundfile: {e}")
    print("  Execute: pip install soundfile")
    sys.exit(1)

# Teste 4: Módulos de atuadores
print("\n[4/7] Testando módulos de atuadores...")
try:
    from fonte_bancada import iniciar_fonte_bancada
    from estacao_solda import iniciar_estacao_solda
    from monitor_energia import iniciar_monitor_energia
    from sensor_temperatura import iniciar_sensor_temperatura
    from registro_tarefas import iniciar_registro_tarefas
    print("  ✅ Todos os atuadores importados")
except Exception as e:
    print(f"  ❌ Erro nos atuadores: {e}")
    sys.exit(1)

# Teste 5: Config JSON
print("\n[5/7] Testando arquivo de configuração...")
try:
    import json
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    print(f"  ✅ Config JSON OK - {len(config['acoes'])} ações configuradas")
except Exception as e:
    print(f"  ❌ Erro no config.json: {e}")
    sys.exit(1)

# Teste 6: PyAudio
print("\n[6/7] Testando PyAudio (microfone)...")
try:
    p = pyaudio.PyAudio()
    info = p.get_default_input_device_info()
    print(f"  ✅ PyAudio OK - Dispositivo: {info['name']}")
    p.terminate()
except Exception as e:
    print(f"  ⚠️  Aviso PyAudio: {e}")
    print("  (Isso pode ser normal se não houver microfone)")

# Teste 7: Modelo pode ser carregado (apenas estrutura)
print("\n[7/7] Testando estrutura do modelo...")
try:
    from inicializador_modelo import MODELOS
    print(f"  ✅ Modelo configurado: {MODELOS[0]}")
    print("  ℹ️  O modelo será baixado na primeira execução (pode demorar)")
except Exception as e:
    print(f"  ❌ Erro: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("✅ TODOS OS TESTES PASSARAM!")
print("="*70)
print("\nPróximos passos:")
print("  1. Grave os áudios: python gravar_audios.py")
print("  2. Execute o assistente: python assistente.py")
print("  3. Execute os testes: python test_assistente.py")
print("\n" + "="*70)
