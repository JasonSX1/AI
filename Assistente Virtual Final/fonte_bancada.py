"""
Módulo para controle da fonte de bancada
Simula uma fonte de alimentação ajustável típica de bancadas de eletrônica
"""
from datetime import datetime

# Estado global da fonte
estado_fonte = {
    "ligada": False,
    "tensao": 0.0,
    "corrente": 0.0,
    "potencia": 0.0
}

def iniciar_fonte_bancada():
    """Inicializa a fonte de bancada"""
    print("[SISTEMA] Fonte de bancada inicializada")
    estado_fonte["ligada"] = False
    estado_fonte["tensao"] = 12.0  # Tensão padrão em Volts
    estado_fonte["corrente"] = 0.0
    estado_fonte["potencia"] = 0.0
    return True

def atuar_sobre_fonte_bancada(acao, dispositivo):
    """
    Controla a fonte de bancada
    
    Args:
        acao: 'ligar' ou 'desligar'
        dispositivo: 'fonte' ou variações
    """
    if dispositivo in ["fonte", "fonte de bancada", "bancada"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if acao == "ligar":
            estado_fonte["ligada"] = True
            estado_fonte["corrente"] = 0.5  # Corrente inicial em Amperes
            estado_fonte["potencia"] = estado_fonte["tensao"] * estado_fonte["corrente"]
            
            print(f"[{timestamp}] FONTE DE BANCADA LIGADA")
            print(f"  └─ Tensão: {estado_fonte['tensao']}V")
            print(f"  └─ Corrente: {estado_fonte['corrente']}A")
            print(f"  └─ Potência: {estado_fonte['potencia']:.2f}W")
            
        elif acao == "desligar":
            estado_fonte["ligada"] = False
            estado_fonte["corrente"] = 0.0
            estado_fonte["potencia"] = 0.0
            
            print(f"[{timestamp}] FONTE DE BANCADA DESLIGADA")
            print(f"  └─ Consumo de energia zerado")
        else:
            print(f"[AVISO] Fonte de bancada não reconhece a ação: {acao}")
    else:
        print(f"[AVISO] Fonte de bancada ignora comando para: {dispositivo}")

def obter_estado_fonte():
    """Retorna o estado atual da fonte"""
    return estado_fonte.copy()
