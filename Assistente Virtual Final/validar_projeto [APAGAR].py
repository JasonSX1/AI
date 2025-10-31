"""
Script de validação do projeto
Verifica se todos os requisitos estão prontos para entrega
"""
import os
import json

print("\n" + "="*70)
print("VALIDADOR DO PROJETO - ASSISTENTE VIRTUAL BANCADA ELETRÔNICA")
print("="*70 + "\n")

# Diretório base
BASE_DIR = r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final"

# Verificações
problemas = []
avisos = []

print("📋 VERIFICANDO ARQUIVOS OBRIGATÓRIOS...\n")

# 1. Arquivos Python principais
arquivos_principais = [
    "assistente.py",
    "config.json",
    "inicializador_modelo.py",
    "inicializador_nltk.py",
    "transcritor.py",
    "test_assistente.py",
    "requirements.txt"
]

for arquivo in arquivos_principais:
    caminho = os.path.join(BASE_DIR, arquivo)
    if os.path.exists(caminho):
        print(f"  ✅ {arquivo}")
    else:
        print(f"  ❌ {arquivo} - FALTANDO!")
        problemas.append(f"Arquivo obrigatório faltando: {arquivo}")

# 2. Módulos de atuadores
print("\n📦 VERIFICANDO MÓDULOS DE ATUADORES...\n")

atuadores = [
    "fonte_bancada.py",
    "estacao_solda.py",
    "monitor_energia.py",
    "sensor_temperatura.py",
    "registro_tarefas.py"
]

for atuador in atuadores:
    caminho = os.path.join(BASE_DIR, atuador)
    if os.path.exists(caminho):
        print(f"  ✅ {atuador}")
    else:
        print(f"  ❌ {atuador} - FALTANDO!")
        problemas.append(f"Módulo atuador faltando: {atuador}")

# 3. Áudios de teste
print("\n🎤 VERIFICANDO ÁUDIOS DE TESTE...\n")

audios_dir = os.path.join(BASE_DIR, "audios")
audios_necessarios = [
    "ligar_fonte.wav",
    "desligar_fonte.wav",
    "ligar_solda.wav",
    "desligar_solda.wav",
    "monitorar_energia.wav",
    "verificar_temperatura.wav",
    "registrar_tarefa.wav"
]

if not os.path.exists(audios_dir):
    print(f"  ❌ Diretório 'audios/' não existe!")
    problemas.append("Diretório de áudios não encontrado")
else:
    for audio in audios_necessarios:
        caminho = os.path.join(audios_dir, audio)
        if os.path.exists(caminho):
            tamanho = os.path.getsize(caminho)
            if tamanho > 0:
                print(f"  ✅ {audio} ({tamanho} bytes)")
            else:
                print(f"  ⚠️  {audio} - ARQUIVO VAZIO!")
                avisos.append(f"Áudio vazio: {audio}")
        else:
            print(f"  ❌ {audio} - FALTANDO!")
            avisos.append(f"Áudio de teste faltando: {audio} - Execute gravar_audios.py")

# 4. Validação do config.json
print("\n⚙️  VERIFICANDO CONFIGURAÇÃO JSON...\n")

config_path = os.path.join(BASE_DIR, "config.json")
try:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    if "acoes" in config:
        print(f"  ✅ Estrutura JSON válida")
        print(f"  ✅ Total de ações configuradas: {len(config['acoes'])}")
        
        # Verifica ações mínimas
        acoes_necessarias = ["ligar", "desligar", "monitorar", "verificar", "registrar"]
        acoes_encontradas = [acao["nome"] for acao in config["acoes"]]
        
        for acao in acoes_necessarias:
            if acao in acoes_encontradas:
                print(f"  ✅ Ação '{acao}' configurada")
            else:
                print(f"  ❌ Ação '{acao}' não encontrada!")
                problemas.append(f"Ação obrigatória faltando no JSON: {acao}")
    else:
        print(f"  ❌ Estrutura JSON inválida!")
        problemas.append("config.json sem campo 'acoes'")
except Exception as e:
    print(f"  ❌ Erro ao ler config.json: {str(e)}")
    problemas.append(f"Erro no config.json: {str(e)}")

# 5. Diretórios necessários
print("\n📂 VERIFICANDO DIRETÓRIOS...\n")

diretorios = ["audios", "temp", "logs", "public"]
for diretorio in diretorios:
    caminho = os.path.join(BASE_DIR, diretorio)
    if os.path.exists(caminho):
        print(f"  ✅ {diretorio}/")
    else:
        print(f"  ⚠️  {diretorio}/ - não existe (será criado automaticamente)")
        avisos.append(f"Diretório '{diretorio}/' não existe")

# 6. Verifica imports proibidos
print("\n🚫 VERIFICANDO CÓDIGO PROIBIDO...\n")

arquivos_para_verificar = ["assistente.py", "transcritor.py", "test_assistente.py"]
imports_proibidos = ["SpeechRecognition", "speech_recognition", "lampada", "som"]

for arquivo in arquivos_para_verificar:
    caminho = os.path.join(BASE_DIR, arquivo)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
            for proibido in imports_proibidos:
                if proibido in conteudo:
                    print(f"  ❌ {arquivo} contém '{proibido}' - PROIBIDO!")
                    problemas.append(f"Código proibido encontrado em {arquivo}: {proibido}")

if not any([p for p in problemas if "proibido" in p.lower()]):
    print(f"  ✅ Nenhum código proibido encontrado")

# Resumo final
print("\n" + "="*70)
print("RESUMO DA VALIDAÇÃO")
print("="*70 + "\n")

if not problemas and not avisos:
    print("  🎉 PROJETO 100% PRONTO PARA ENTREGA!")
    print("\n  ✅ Todos os arquivos obrigatórios presentes")
    print("  ✅ Todos os atuadores implementados")
    print("  ✅ Todos os áudios de teste presentes")
    print("  ✅ Configuração JSON válida")
    print("  ✅ Sem código proibido")
elif not problemas:
    print("  ✅ PROJETO PRONTO COM AVISOS")
    print(f"\n  Total de avisos: {len(avisos)}")
    for aviso in avisos:
        print(f"    ⚠️  {aviso}")
else:
    print("  ❌ PROJETO COM PROBLEMAS - CORREÇÃO NECESSÁRIA")
    print(f"\n  Total de problemas: {len(problemas)}")
    for problema in problemas:
        print(f"    ❌ {problema}")
    
    if avisos:
        print(f"\n  Total de avisos: {len(avisos)}")
        for aviso in avisos:
            print(f"    ⚠️  {aviso}")

# Próximos passos
print("\n" + "="*70)
print("PRÓXIMOS PASSOS")
print("="*70 + "\n")

if avisos and "Áudio" in str(avisos):
    print("  1. ❗ Execute: python gravar_audios.py")
    print("     (Para gravar os áudios de teste necessários)")

print("  2. 🧪 Execute: python test_assistente.py")
print("     (Para validar o funcionamento dos testes)")

print("  3. 🚀 Execute: python assistente.py")
print("     (Para testar o assistente completo)")

print("  4. 🎥 Grave o vídeo de apresentação")
print("     (Demonstrando tema, testes e funcionamento)")

print("  5. 📤 Entregue pelo CLASSROOM")
print("     (Código-fonte + vídeo até 31/10/2026)")

print("\n" + "="*70 + "\n")
