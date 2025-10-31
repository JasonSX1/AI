"""
Módulo para controle da estação de solda
Simula uma estação de solda com controle de temperatura
"""
from datetime import datetime
import random

# Estado global da estação
estado_estacao = {
    "ligada": False,
    "temperatura_alvo": 350,  # Celsius
    "temperatura_atual": 25,  # Temperatura ambiente
    "pronta": False
}

def iniciar_estacao_solda():
    """Inicializa a estação de solda"""
    print("[SISTEMA] Estação de solda inicializada")
    estado_estacao["ligada"] = False
    estado_estacao["temperatura_atual"] = 25
    estado_estacao["pronta"] = False
    return True

def atuar_sobre_estacao_solda(acao, dispositivo):
    """
    Controla a estação de solda
    
    Args:
        acao: 'ligar' ou 'desligar'
        dispositivo: 'solda', 'estação' ou variações
    """
    if dispositivo in ["solda", "estação", "estação de solda", "ferro"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if acao == "ligar":
            estado_estacao["ligada"] = True
            # Simula aquecimento gradual
            estado_estacao["temperatura_atual"] = random.randint(320, 350)
            estado_estacao["pronta"] = True
            
            print(f"[{timestamp}] ESTAÇÃO DE SOLDA LIGADA")
            print(f"  └─ Temperatura alvo: {estado_estacao['temperatura_alvo']}°C")
            print(f"  └─ Aquecendo... Temperatura atual: {estado_estacao['temperatura_atual']}°C")
            print(f"  └─ Status: {'PRONTA PARA USO' if estado_estacao['pronta'] else 'AQUECENDO'}")
            
        elif acao == "desligar":
            estado_estacao["ligada"] = False
            estado_estacao["pronta"] = False
            temp_resfriamento = random.randint(40, 80)
            
            print(f"[{timestamp}] ESTAÇÃO DE SOLDA DESLIGADA")
            print(f"  └─ Resfriando... Temperatura atual: {temp_resfriamento}°C")
            print(f"  └─ ATENÇÃO: Aguarde resfriamento completo antes de guardar")
            
            estado_estacao["temperatura_atual"] = temp_resfriamento
        else:
            print(f"[AVISO] Estação de solda não reconhece a ação: {acao}")
    else:
        print(f"[AVISO] Estação de solda ignora comando para: {dispositivo}")

def obter_estado_estacao():
    """Retorna o estado atual da estação"""
    return estado_estacao.copy()
