from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_most_frequent_response

def configurar_robo():
    """Configura e retorna uma instância do ChatterBot"""
    robo = ChatBot(
        "AssistenteBancada",
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Desculpe, não entendi. Pode reformular a pergunta?',
                'maximum_similarity_threshold': 0.70
            }
        ],
        database_uri='sqlite:///db.sqlite3'
    )
    return robo
