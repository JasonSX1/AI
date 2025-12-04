import unittest
import os
from bot import configurar_robo
from treinamento import configurar_treinador, carregar_conversas, treinar

class TestAssistenteOficina(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura o ambiente de teste"""
        if os.path.exists("db.sqlite3"):
            os.remove("db.sqlite3")
        
        print("Treinando robô para testes...")
        treinador = configurar_treinador()
        conversas = carregar_conversas()
        treinar(treinador, conversas)
        cls.robo = configurar_robo()

    def test_01_saudacao(self):
        """Teste de saudação"""
        resposta = self.robo.get_response("olá")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Saudação: {resposta.text}")

    def test_02_horario(self):
        """Teste sobre horário"""
        resposta = self.robo.get_response("qual o horario de funcionamento?")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Horário: {resposta.text}")

    def test_03_garantia(self):
        """Teste sobre garantia"""
        resposta = self.robo.get_response("tem garantia?")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Garantia: {resposta.text}")

    def test_04_backup(self):
        """Teste sobre backup"""
        resposta = self.robo.get_response("preciso fazer backup?")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Backup: {resposta.text}")

    def test_05_orcamento(self):
        """Teste sobre orçamento"""
        resposta = self.robo.get_response("o orcamento é gratuito?")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Orçamento: {resposta.text}")

    def test_06_status_os(self):
        """Teste de Status de OS"""
        resposta = self.robo.get_response("status os 1001")
        self.assertGreaterEqual(resposta.confidence, 0.6)
        print(f"Teste Status OS: {resposta.text}")

if __name__ == "__main__":
    unittest.main()
