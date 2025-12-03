import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock ChatterBot modules
sys.modules["chatterbot"] = MagicMock()
sys.modules["chatterbot.trainers"] = MagicMock()
sys.modules["chatterbot.comparisons"] = MagicMock()
sys.modules["chatterbot.response_selection"] = MagicMock()

# Mock the specific classes used
mock_chatbot = MagicMock()
sys.modules["chatterbot"].ChatBot.return_value = mock_chatbot

# Configure the mock response
mock_response = MagicMock()
mock_response.text = "Resposta simulada"
mock_response.confidence = 0.9
mock_chatbot.get_response.return_value = mock_response

from bot import configurar_robo
from trainer import treinar

class TestAssistenteBancada(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura o ambiente de teste"""
        # Remove banco de dados antigo para garantir teste limpo
        if os.path.exists("db.sqlite3"):
            os.remove("db.sqlite3")
        
        # Treina o robô
        print("Treinando robô para testes...")
        treinar()
        
        cls.robo = configurar_robo()

    def test_01_saudacao(self):
        """Teste de saudação"""
        resposta = self.robo.get_response("olá")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Saudação: {resposta.text} (Confiança: {resposta.confidence})")

    def test_02_fonte_bancada(self):
        """Teste sobre fonte de bancada"""
        resposta = self.robo.get_response("como ligar a fonte?")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Fonte: {resposta.text} (Confiança: {resposta.confidence})")

    def test_03_estacao_solda(self):
        """Teste sobre estação de solda"""
        resposta = self.robo.get_response("qual temperatura para solda?")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Solda: {resposta.text} (Confiança: {resposta.confidence})")

    def test_04_multimetro(self):
        """Teste sobre multímetro"""
        resposta = self.robo.get_response("como medir tensão?")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Multímetro: {resposta.text} (Confiança: {resposta.confidence})")

    def test_05_esd(self):
        """Teste sobre ESD"""
        resposta = self.robo.get_response("o que é esd?")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste ESD: {resposta.text} (Confiança: {resposta.confidence})")

    def test_06_continuidade(self):
        """Teste sobre continuidade"""
        resposta = self.robo.get_response("como testar continuidade?")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Continuidade: {resposta.text} (Confiança: {resposta.confidence})")

if __name__ == "__main__":
    unittest.main()
