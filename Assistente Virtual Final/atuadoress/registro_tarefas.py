import json
import os
from datetime import datetime

ARQUIVO_TAREFAS = "tarefas_reparo.json" 

def iniciar_registro_tarefas():
    """Inicializa o módulo e cria o arquivo JSON se não existir."""
    print("[SISTEMA] Módulo de registro de tarefas inicializado.")
    if not os.path.exists(ARQUIVO_TAREFAS):
        try:
            with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
                json.dump([], f) # Cria uma lista vazia no arquivo
            print(f"Arquivo {ARQUIVO_TAREFAS} criado.")
        except Exception as e:
            print(f"[ERRO] Não foi possível criar {ARQUIVO_TAREFAS}: {e}")
            return False
    return True

def atuar_sobre_registro_tarefas(acao, dispositivo):
    """
    Salva uma nova tarefa de reparo no arquivo JSON.
    
    Args:
        acao (str): Ação a ser executada. Espera-se "registrar".
        dispositivo (str): O texto completo da descrição da tarefa.
    """
    
    # --- ESTA É A CORREÇÃO ---
    # Se a ação é registrar, o 'dispositivo' é o *texto* da tarefa.
    # Não precisamos mais validar o nome do dispositivo.
    
    if acao == "registrar":
        try:
            # Carrega as tarefas existentes
            with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
                tarefas = json.load(f)
            
            # Cria a nova tarefa
            nova_tarefa = {
                "id": len(tarefas) + 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "descricao": dispositivo, # O 'dispositivo' É a descrição
                "status": "pendente"
            }
            
            # Adiciona e salva
            tarefas.append(nova_tarefa)
            with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
                json.dump(tarefas, f, indent=4, ensure_ascii=False)
            
            print(f"[REGISTRO] Tarefa salva: {dispositivo[:50]}...")
            return {
                "sucesso": True,
                "mensagem": "✅ Tarefa registrada com sucesso!"
            }
        
        except Exception as e:
            print(f"[ERRO] Falha ao salvar tarefa no JSON: {e}")
            return {
                "sucesso": False,
                "mensagem": f"Erro ao salvar arquivo: {e}"
            }

    else:
        mensagem = f"⚠️ Sistema de registro ignora comando para: {dispositivo}"
        print(f"[AVISO] {mensagem}")
        return {"sucesso": False, "mensagem": mensagem}