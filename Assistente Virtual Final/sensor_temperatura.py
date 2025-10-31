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
        
    Returns:
        dict: Resultado da operação com status e mensagem
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
            
            # Verifica alertas
            alerta_fonte = temp_fonte >= TEMP_MAXIMA_FONTE
            alerta_estacao = estacao["ligada"] and temp_estacao > TEMP_MAXIMA_ESTACAO
            
            # Monta mensagem
            mensagem = f"""🌡️ LEITURA DE SENSORES
  • Temperatura ambiente: {temp_ambiente}°C
  • Fonte: {temp_fonte}°C - {'⚠️ ALERTA!' if alerta_fonte else '✅ Normal'}
  • Estação: {temp_estacao}°C - {'⚠️ SUPERAQUECIMENTO!' if alerta_estacao else '✅ Normal' if estacao['ligada'] else '✅ Desligada'}
  ━━━━━━━━━━━━━━━━━━━━━━━━━━
  {'⚠️ ATENÇÃO NECESSÁRIA' if (alerta_fonte or alerta_estacao) else '✅ PARÂMETROS NORMAIS'}"""
            
            print(f"\n{'='*50}")
            print(f"[{timestamp}] {mensagem}")
            print(f"{'='*50}\n")
            
            return {
                "sucesso": True,
                "mensagem": mensagem,
                "temp_ambiente": temp_ambiente,
                "temp_fonte": temp_fonte,
                "temp_estacao": temp_estacao,
                "alerta": alerta_fonte or alerta_estacao
            }
        else:
            mensagem = f"⚠️ Sensor de temperatura não reconhece a ação: {acao}"
            print(f"[AVISO] {mensagem}")
            return {"sucesso": False, "mensagem": mensagem}
    else:
        mensagem = f"⚠️ Sensor de temperatura ignora comando para: {dispositivo}"
        print(f"[AVISO] {mensagem}")
        return {"sucesso": False, "mensagem": mensagem}
