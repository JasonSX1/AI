import json
import os
from difflib import get_close_matches

class MockResponse:
    def __init__(self, text, confidence):
        self.text = text
        self.confidence = confidence
    
    def __str__(self):
        return self.text

class MockChatBot:
    def __init__(self, name, **kwargs):
        self.name = name
        self.knowledge_base = {}
        self.load_initial_data()

    def load_initial_data(self):
        # Tenta carregar dados dos arquivos json para ter respostas reais
        try:
            config_dir = os.path.join(os.path.dirname(__file__), 'config')
            if os.path.exists(config_dir):
                for filename in os.listdir(config_dir):
                    if filename.endswith('.json'):
                        with open(os.path.join(config_dir, filename), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            for conv in data.get('conversas', []):
                                response = conv['resposta']
                                for msg in conv['mensagens']:
                                    self.knowledge_base[msg.lower()] = response
        except Exception as e:
            print(f"Erro ao carregar dados mock: {e}")

    def get_response(self, text):
        text = text.lower()
        
        # Busca exata
        if text in self.knowledge_base:
            return MockResponse(self.knowledge_base[text], 1.0)
        
        # Busca aproximada
        matches = get_close_matches(text, self.knowledge_base.keys(), n=1, cutoff=0.6)
        if matches:
            return MockResponse(self.knowledge_base[matches[0]], 0.8)
            
        return MockResponse("Desculpe, não entendi. (Modo de Compatibilidade Python 3.14)", 0.0)

def configurar_robo():
    print("⚠️  AVISO: Usando MockChatBot devido a erro de importação do ChatterBot.")
    return MockChatBot("AssistenteBancada")
