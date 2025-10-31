"""
Módulo para monitoramento de energia da bancada
Calcula e exibe consumo energético dos equipamentos
"""
from datetime import datetime
from fonte_bancada import obter_estado_fonte
from estacao_solda import obter_estado_estacao

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
    """
    if dispositivo in ["energia", "consumo", "watts", "potência"]:
        if acao in ["monitorar", "verificar", "medir", "checar"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Obtém estados dos equipamentos
            fonte = obter_estado_fonte()
            estacao = obter_estado_estacao()
            
            # Calcula consumo total
            consumo_total = CONSUMO_BASE_BANCADA
            
            if fonte["ligada"]:
                consumo_total += fonte["potencia"]
            
            if estacao["ligada"]:
                consumo_total += CONSUMO_ESTACAO_SOLDA
            
            # Exibe relatório
            print(f"\n{'='*50}")
            print(f"[{timestamp}] RELATÓRIO DE CONSUMO ENERGÉTICO")
            print(f"{'='*50}")
            print(f"  📊 Consumo base da bancada: {CONSUMO_BASE_BANCADA}W")
            
            if fonte["ligada"]:
                print(f"  🔌 Fonte de bancada: {fonte['potencia']:.2f}W (LIGADA)")
            else:
                print(f"  🔌 Fonte de bancada: 0W (DESLIGADA)")
            
            if estacao["ligada"]:
                print(f"  🔥 Estação de solda: {CONSUMO_ESTACAO_SOLDA}W (LIGADA)")
            else:
                print(f"  🔥 Estação de solda: 0W (DESLIGADA)")
            
            print(f"  {'─'*46}")
            print(f"  ⚡ CONSUMO TOTAL: {consumo_total:.2f}W")
            print(f"  💡 Estimativa mensal (8h/dia): {(consumo_total * 8 * 30 / 1000):.2f} kWh")
            print(f"{'='*50}\n")
        else:
            print(f"[AVISO] Monitor de energia não reconhece a ação: {acao}")
    else:
        print(f"[AVISO] Monitor de energia ignora comando para: {dispositivo}")
