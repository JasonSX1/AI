from chatterbot import ChatBot
try:
    from chatterbot.trainers import ListTrainer
    from bot import configurar_robo
except Exception as e:
    print(f"⚠️  Erro ao importar ChatterBot: {e}")
    from mock_bot import configurar_robo
    # Mock ListTrainer
    class ListTrainer:
        def __init__(self, robo): pass
        def train(self, data): pass
import json
import os

def carregar_conversas():
    """Carrega conversas dos arquivos JSON na pasta config"""
    conversas = []
    caminho_config = os.path.join(os.path.dirname(__file__), 'config')
    
    for arquivo in os.listdir(caminho_config):
        if arquivo.endswith('.json'):
            caminho_arquivo = os.path.join(caminho_config, arquivo)
            print(f"Carregando: {arquivo}")
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                if "conversas" in dados:
                    conversas.extend(dados["conversas"])
    return conversas

def treinar():
    """Treina o robô com as conversas carregadas"""
    robo = configurar_robo()
    treinador = ListTrainer(robo)
    
    conversas_data = carregar_conversas()
    
    print("Iniciando treinamento...")
    for item in conversas_data:
        mensagens = item["mensagens"]
        resposta = item["resposta"]
        
        for mensagem in mensagens:
            # Treina a pergunta com a resposta
            treinador.train([mensagem, resposta])
            
    print("Treinamento concluído!")

if __name__ == "__main__":
    treinar()
