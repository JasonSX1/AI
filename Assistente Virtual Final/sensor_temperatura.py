"""
Módulo para verificação de temperatura dos equipamentos
Simula sensores de temperatura e emite alertas
"""
from datetime import datetime
import random
from fonte_bancada import obter_estado_fonte
from estacao_solda import obter_estado_estacao

# Limites de temperatura para alertas
TEMP_MAXIMA_FONTE = 60      # °C
TEMP_MAXIMA_ESTACAO = 400   # °C
TEMP_ALERTA_AMBIENTE = 35   # °C

def iniciar_sensor_temperatura():
    """Inicializa o sensor de temperatura"""
    print("[SISTEMA] Sensor de temperatura inicializado")
    return True

def atuar_sobre_sensor_temperatura(acao, dispositivo):
    """
    Verifica temperatura dos equipamentos
    
    Args:
        acao: 'verificar', 'medir', 'checar'
        dispositivo: 'temperatura', 'calor', 'equipamentos'
    """
    if dispositivo in ["temperatura", "calor", "equipamentos", "aquecimento"]:
        if acao in ["verificar", "medir", "checar", "monitorar"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Obtém estados dos equipamentos
            fonte = obter_estado_fonte()
            estacao = obter_estado_estacao()
            
            # Simula leituras de temperatura
            temp_ambiente = random.randint(22, 28)
            
            if fonte["ligada"]:
                temp_fonte = random.randint(35, 55)
            else:
                temp_fonte = temp_ambiente
            
            if estacao["ligada"]:
                temp_estacao = estacao["temperatura_atual"]
            else:
                temp_estacao = temp_ambiente
            
            # Exibe relatório
            print(f"\n{'='*50}")
            print(f"[{timestamp}] LEITURA DE SENSORES DE TEMPERATURA")
            print(f"{'='*50}")
            print(f"  🌡️  Temperatura ambiente: {temp_ambiente}°C")
            
            # Fonte de bancada
            status_fonte = "✅ NORMAL" if temp_fonte < TEMP_MAXIMA_FONTE else "⚠️  ALERTA!"
            print(f"  🔌 Fonte de bancada: {temp_fonte}°C - {status_fonte}")
            
            if temp_fonte >= TEMP_MAXIMA_FONTE:
                print(f"     ⚠️  ATENÇÃO: Temperatura acima do limite seguro ({TEMP_MAXIMA_FONTE}°C)")
                print(f"     ⚠️  Recomendação: Desligue e aguarde resfriamento")
            
            # Estação de solda
            if estacao["ligada"]:
                if temp_estacao > TEMP_MAXIMA_ESTACAO:
                    status_estacao = "⚠️  SUPERAQUECIMENTO!"
                    print(f"  🔥 Estação de solda: {temp_estacao}°C - {status_estacao}")
                    print(f"     ⚠️  PERIGO: Temperatura crítica detectada!")
                else:
                    status_estacao = "✅ OPERACIONAL"
                    print(f"  🔥 Estação de solda: {temp_estacao}°C - {status_estacao}")
            else:
                print(f"  🔥 Estação de solda: {temp_estacao}°C - ✅ DESLIGADA")
            
            # Alerta geral
            print(f"  {'─'*46}")
            if temp_fonte >= TEMP_MAXIMA_FONTE or temp_estacao > TEMP_MAXIMA_ESTACAO:
                print(f"  ⚠️  STATUS GERAL: ATENÇÃO NECESSÁRIA")
            else:
                print(f"  ✅ STATUS GERAL: TODOS OS PARÂMETROS NORMAIS")
            print(f"{'='*50}\n")
        else:
            print(f"[AVISO] Sensor de temperatura não reconhece a ação: {acao}")
    else:
        print(f"[AVISO] Sensor de temperatura ignora comando para: {dispositivo}")
