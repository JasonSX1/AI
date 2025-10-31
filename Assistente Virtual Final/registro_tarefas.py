"""
Módulo para registro de tarefas e reparos
Armazena logs de operações realizadas na bancada
"""
from datetime import datetime
import os
import json

# Caminho para o arquivo de logs
CAMINHO_LOG = "logs"
ARQUIVO_TAREFAS = os.path.join(CAMINHO_LOG, "tarefas_reparo.json")

def iniciar_registro_tarefas():
    """Inicializa o sistema de registro de tarefas"""
    # Cria diretório de logs se não existir
    if not os.path.exists(CAMINHO_LOG):
        os.makedirs(CAMINHO_LOG)
        print(f"[SISTEMA] Diretório de logs criado: {CAMINHO_LOG}")
    
    # Cria arquivo de tarefas se não existir
    if not os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
            json.dump({"tarefas": []}, f, ensure_ascii=False, indent=2)
        print(f"[SISTEMA] Arquivo de tarefas criado: {ARQUIVO_TAREFAS}")
    
    print("[SISTEMA] Sistema de registro de tarefas inicializado")
    return True

def atuar_sobre_registro_tarefas(acao, dispositivo):
    """
    Registra tarefas e reparos realizados
    
    Args:
        acao: 'registrar', 'anotar', 'salvar'
        dispositivo: 'tarefa', 'reparo', 'manutenção'
    """
    if dispositivo in ["tarefa", "reparo", "manutenção", "registro", "log"]:
        if acao in ["registrar", "anotar", "salvar", "gravar"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = datetime.now().strftime("%d/%m/%Y")
            hora = datetime.now().strftime("%H:%M:%S")
            
            # Descrições de exemplo (em produção real, isso viria do comando de voz)
            descricoes_exemplo = [
                "Reparo de placa-mãe - substituição de capacitor eletrolítico",
                "Teste de fonte de notebook - verificação de tensões",
                "Soldagem de componentes SMD - reparo em smartphone",
                "Diagnóstico de curto-circuito em placa de TV",
                "Recondicionamento de bateria - substituição de células"
            ]
            
            import random
            descricao = random.choice(descricoes_exemplo)
            
            # Lê tarefas existentes
            try:
                with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            except:
                dados = {"tarefas": []}
            
            # Adiciona nova tarefa
            nova_tarefa = {
                "id": len(dados["tarefas"]) + 1,
                "data": data,
                "hora": hora,
                "descricao": descricao,
                "timestamp": timestamp
            }
            
            dados["tarefas"].append(nova_tarefa)
            
            # Salva no arquivo
            with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            # Exibe confirmação
            print(f"\n{'='*50}")
            print(f"[{timestamp}] NOVA TAREFA REGISTRADA")
            print(f"{'='*50}")
            print(f"  📋 ID da tarefa: #{nova_tarefa['id']}")
            print(f"  📅 Data: {data}")
            print(f"  🕐 Hora: {hora}")
            print(f"  📝 Descrição: {descricao}")
            print(f"  💾 Salvo em: {ARQUIVO_TAREFAS}")
            print(f"{'='*50}\n")
            
            # Mostra total de tarefas
            print(f"  ℹ️  Total de tarefas registradas: {len(dados['tarefas'])}")
            
        else:
            print(f"[AVISO] Sistema de registro não reconhece a ação: {acao}")
    else:
        print(f"[AVISO] Sistema de registro ignora comando para: {dispositivo}")

def listar_tarefas():
    """Lista todas as tarefas registradas"""
    try:
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        if dados["tarefas"]:
            print(f"\n{'='*50}")
            print("HISTÓRICO DE TAREFAS E REPAROS")
            print(f"{'='*50}")
            for tarefa in dados["tarefas"]:
                print(f"\n  #{tarefa['id']} - {tarefa['data']} às {tarefa['hora']}")
                print(f"  └─ {tarefa['descricao']}")
            print(f"\n{'='*50}\n")
        else:
            print("[INFO] Nenhuma tarefa registrada ainda")
    except:
        print("[ERRO] Não foi possível ler o arquivo de tarefas")
