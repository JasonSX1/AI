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
        
    Returns:
        dict: Resultado da operação com status e mensagem
    """
    if dispositivo in ["fonte", "fonte de bancada", "bancada"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if acao == "ligar":
            # Verifica se já está ligada
            if estado_fonte["ligada"]:
                mensagem = "⚠️ FONTE JÁ ESTÁ LIGADA"
                print(f"[{timestamp}] {mensagem}")
                return {"sucesso": False, "mensagem": mensagem, "estado": estado_fonte.copy()}
            
            estado_fonte["ligada"] = True
            estado_fonte["corrente"] = 0.5  # Corrente inicial em Amperes
            estado_fonte["potencia"] = estado_fonte["tensao"] * estado_fonte["corrente"]
            
            mensagem = f"✅ FONTE DE BANCADA LIGADA\n  └─ Tensão: {estado_fonte['tensao']}V\n  └─ Corrente: {estado_fonte['corrente']}A\n  └─ Potência: {estado_fonte['potencia']:.2f}W"
            print(f"[{timestamp}] {mensagem}")
            return {"sucesso": True, "mensagem": mensagem, "estado": estado_fonte.copy()}
            
        elif acao == "desligar":
            # Verifica se já está desligada
            if not estado_fonte["ligada"]:
                mensagem = "⚠️ FONTE JÁ ESTÁ DESLIGADA"
                print(f"[{timestamp}] {mensagem}")
                return {"sucesso": False, "mensagem": mensagem, "estado": estado_fonte.copy()}
            
            estado_fonte["ligada"] = False
            estado_fonte["corrente"] = 0.0
            estado_fonte["potencia"] = 0.0
            
            mensagem = "✅ FONTE DE BANCADA DESLIGADA\n  └─ Consumo de energia zerado"
            print(f"[{timestamp}] {mensagem}")
            return {"sucesso": True, "mensagem": mensagem, "estado": estado_fonte.copy()}
        else:
            mensagem = f"⚠️ Fonte de bancada não reconhece a ação: {acao}"
            print(f"[AVISO] {mensagem}")
            return {"sucesso": False, "mensagem": mensagem, "estado": estado_fonte.copy()}
    else:
        mensagem = f"⚠️ Fonte de bancada ignora comando para: {dispositivo}"
        print(f"[AVISO] {mensagem}")
        return {"sucesso": False, "mensagem": mensagem, "estado": estado_fonte.copy()}

def obter_estado_fonte():
    """Retorna o estado atual da fonte"""
    return estado_fonte.copy()
