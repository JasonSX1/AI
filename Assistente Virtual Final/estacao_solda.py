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
        
    Returns:
        dict: Resultado da operação com status e mensagem
    """
    if dispositivo in ["solda", "estação", "estação de solda", "ferro"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if acao == "ligar":
            # Verifica se já está ligada
            if estado_estacao["ligada"]:
                mensagem = "⚠️ ESTAÇÃO DE SOLDA JÁ ESTÁ LIGADA"
                print(f"[{timestamp}] {mensagem}")
                return {"sucesso": False, "mensagem": mensagem, "estado": estado_estacao.copy()}
            
            estado_estacao["ligada"] = True
            # Simula aquecimento gradual
            estado_estacao["temperatura_atual"] = random.randint(320, 350)
            estado_estacao["pronta"] = True
            
            mensagem = f"✅ ESTAÇÃO DE SOLDA LIGADA\n  └─ Temperatura alvo: {estado_estacao['temperatura_alvo']}°C\n  └─ Temperatura atual: {estado_estacao['temperatura_atual']}°C\n  └─ Status: PRONTA PARA USO"
            print(f"[{timestamp}] {mensagem}")
            return {"sucesso": True, "mensagem": mensagem, "estado": estado_estacao.copy()}
            
        elif acao == "desligar":
            # Verifica se já está desligada
            if not estado_estacao["ligada"]:
                mensagem = "⚠️ ESTAÇÃO DE SOLDA JÁ ESTÁ DESLIGADA"
                print(f"[{timestamp}] {mensagem}")
                return {"sucesso": False, "mensagem": mensagem, "estado": estado_estacao.copy()}
            
            estado_estacao["ligada"] = False
            estado_estacao["pronta"] = False
            temp_resfriamento = random.randint(40, 80)
            
            mensagem = f"✅ ESTAÇÃO DE SOLDA DESLIGADA\n  └─ Resfriando... Temperatura: {temp_resfriamento}°C\n  └─ ATENÇÃO: Aguarde resfriamento"
            print(f"[{timestamp}] {mensagem}")
            
            estado_estacao["temperatura_atual"] = temp_resfriamento
            return {"sucesso": True, "mensagem": mensagem, "estado": estado_estacao.copy()}
        else:
            mensagem = f"⚠️ Estação de solda não reconhece a ação: {acao}"
            print(f"[AVISO] {mensagem}")
            return {"sucesso": False, "mensagem": mensagem, "estado": estado_estacao.copy()}
    else:
        mensagem = f"⚠️ Estação de solda ignora comando para: {dispositivo}"
        print(f"[AVISO] {mensagem}")
        return {"sucesso": False, "mensagem": mensagem, "estado": estado_estacao.copy()}

def obter_estado_estacao():
    """Retorna o estado atual da estação"""
    return estado_estacao.copy()
