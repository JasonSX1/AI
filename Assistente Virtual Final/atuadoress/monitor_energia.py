"""
Módulo para monitoramento de energia da bancada
Calcula e exibe consumo energético dos equipamentos
"""
from datetime import datetime
from atuadoress.fonte_bancada import obter_estado_fonte
from atuadoress.estacao_solda import obter_estado_estacao

# Consumos típicos em Watts
CONSUMO_ESTACAO_SOLDA = 60  # 60W quando ligada
CONSUMO_BASE_BANCADA = 5    # Consumo base da bancada

def iniciar_monitor_energia():
    """Inicializa o monitor de energia"""
    print("[SISTEMA] Monitor de energia inicializado")
    return True

def atuar_sobre_monitor_energia(acao, dispositivo):
    """
    Monitora e exibe o consumo de energia
    
    Args:
        acao: 'monitorar', 'verificar', 'medir'
        dispositivo: 'energia', 'consumo'
        
    Returns:
        dict: Resultado da operação com status e mensagem
    """
    if dispositivo in ["energia", "consumo", "watts", "potência"]:
        if acao in ["monitorar", "verificar", "medir", "checar"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Obtém estados dos equipamentos
            fonte = obter_estado_fonte()
            estacao = obter_estado_estacao()
            
            # Calcula consumo total
            consumo_total = CONSUMO_BASE_BANCADA
            
            consumo_fonte = fonte["potencia"] if fonte["ligada"] else 0
            consumo_estacao = CONSUMO_ESTACAO_SOLDA if estacao["ligada"] else 0
            
            consumo_total += consumo_fonte + consumo_estacao
            
            # Monta mensagem formatada
            mensagem = f"""📊 RELATÓRIO DE CONSUMO ENERGÉTICO
  • Consumo base: {CONSUMO_BASE_BANCADA}W
  • Fonte de bancada: {consumo_fonte:.2f}W ({'LIGADA' if fonte['ligada'] else 'DESLIGADA'})
  • Estação de solda: {consumo_estacao}W ({'LIGADA' if estacao['ligada'] else 'DESLIGADA'})
  ━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚡ CONSUMO TOTAL: {consumo_total:.2f}W
  � Estimativa mensal: {(consumo_total * 8 * 30 / 1000):.2f} kWh"""
            
            print(f"\n{'='*50}")
            print(f"[{timestamp}] {mensagem}")
            print(f"{'='*50}\n")
            
            return {
                "sucesso": True,
                "mensagem": mensagem,
                "consumo_total": consumo_total,
                "consumo_fonte": consumo_fonte,
                "consumo_estacao": consumo_estacao
            }
        else:
            mensagem = f"⚠️ Monitor de energia não reconhece a ação: {acao}"
            print(f"[AVISO] {mensagem}")
            return {"sucesso": False, "mensagem": mensagem}
    else:
        mensagem = f"⚠️ Monitor de energia ignora comando para: {dispositivo}"
        print(f"[AVISO] {mensagem}")
        return {"sucesso": False, "mensagem": mensagem}
