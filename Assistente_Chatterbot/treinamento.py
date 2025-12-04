from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
import os

NOME_ROBO = "AssistenteBancada"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

CONVERSAS = [
    os.path.join(CONFIG_DIR, "saudacoes.json"),
    os.path.join(CONFIG_DIR, "atendimento.json")
]

def configurar_treinador():
    """Cria o chatbot e o treinador"""
    # Configuração adaptada para manter a persistência do banco se possível
    try:
        robo = ChatBot(
            NOME_ROBO,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'Desculpe, não entendi.',
                    'maximum_similarity_threshold': 0.70
                }
            ],
            database_uri='sqlite:///db.sqlite3'
        )
    except:
        # Fallback para instanciação simples (Mock)
        robo = ChatBot(NOME_ROBO)
        
    treinador = ListTrainer(robo)
    return treinador

def carregar_conversas():
    """Carrega as conversas a partir dos arquivos JSON"""
    conversas = []
    for arquivo_conversas in CONVERSAS:
        if os.path.exists(arquivo_conversas):
            with open(arquivo_conversas, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                conversas.append(dados["conversas"])
        else:
            print(f"⚠️ Arquivo não encontrado: {arquivo_conversas}")
    return conversas

def treinar(treinador, conversas):
    """Treina o chatbot com as mensagens e respostas"""
    for conversa in conversas:
        for mensagens_resposta in conversa:
            mensagens = mensagens_resposta["mensagens"]
            resposta = mensagens_resposta["resposta"]

            for mensagem in mensagens:
                print(f"Treinando mensagem: '{mensagem}' -> '{resposta}'")
                treinador.train([mensagem.lower(), resposta])

if __name__ == "__main__":
    treinador = configurar_treinador()
    conversas = carregar_conversas()

    if treinador and conversas:
        treinar(treinador, conversas)
        print("\n✅ Treinamento concluído com sucesso!")
    else:
        print("\n⚠️ Nenhuma conversa encontrada para treinar.")
