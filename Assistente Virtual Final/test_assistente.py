import unittest
import torch
import os
import json
from transcritor import carregar_fala, transcrever_fala, iniciar_modelo, MODELO
from assistente import processar_transcricao, validar_comando
from nltk import corpus

# Configurações
CAMINHO_AUDIOS = r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\audios"
CONFIGURACOES = r"c:\Users\Usuario\Desktop\AI\Assistente Virtual Final\config.json"

class TestAssistenteVirtual(unittest.TestCase):
    """Testes para o assistente virtual de bancada eletrônica"""
    
    @classmethod
    def setUpClass(cls):
        """Configuração inicial executada uma vezantes  de todos os testes"""
        print("\n" + "="*70)
        print("INICIANDO TESTES DO ASSISTENTE VIRTUAL - BANCADA ELETRÔNICA")
        print("="*70 + "\n")
        
        # Inicializa o modelo de reconhecimento
        cls.dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"
        print(f"Dispositivo utilizado: {cls.dispositivo}")
        
        iniciado, cls.processador, cls.modelo = iniciar_modelo(MODELO, cls.dispositivo)
        if not iniciado:
            raise Exception("Falha ao inicializar o modelo de reconhecimento de fala")
        
        print("✓ Modelo de reconhecimento inicializado com sucesso")
        
        # Carrega palavras de parada
        cls.palavras_de_parada = set(corpus.stopwords.words("portuguese"))
        print("✓ Palavras de parada carregadas")
        
        # Carrega configurações
        with open(CONFIGURACOES, "r", encoding="utf-8") as f:
            configuracoes = json.load(f)
            cls.acoes = configuracoes["acoes"]
        print("✓ Configurações carregadas do JSON")
        
        print("\n" + "-"*70 + "\n")
    
    def setUp(self):
        """Configuração executada antes de cada teste"""
        pass
    
    def _testar_comando_audio(self, arquivo_audio, comando_esperado, acao_esperada, dispositivo_esperado):
        """
        Método auxiliar para testar um comando de áudio
        
        Args:
            arquivo_audio: Nome do arquivo de áudio
            comando_esperado: Comando que deveria ser reconhecido
            acao_esperada: Ação esperada do comando
            dispositivo_esperado: Dispositivo esperado do comando
        """
        caminho_completo = os.path.join(CAMINHO_AUDIOS, arquivo_audio)
        
        print(f"\nTestando: {comando_esperado}")
        print(f"Arquivo: {arquivo_audio}")
        
        # Verifica se o arquivo existe
        self.assertTrue(
            os.path.exists(caminho_completo),
            f"Arquivo de áudio não encontrado: {caminho_completo}"
        )
        
        # Carrega e transcreve o áudio
        fala = carregar_fala(caminho_completo)
        transcricao = transcrever_fala(self.dispositivo, fala, self.modelo, self.processador)
        print(f"Transcrição: '{transcricao}'")
        
        # Processa a transcrição
        comando = processar_transcricao(transcricao, self.palavras_de_parada)
        print(f"Comando processado: {comando}")
        
        # Valida o comando
        valido, acao, dispositivo = validar_comando(comando, self.acoes)
        
        print(f"Validação: {'✓ VÁLIDO' if valido else '✗ INVÁLIDO'}")
        if valido:
            print(f"Ação: {acao}")
            print(f"Dispositivo: {dispositivo}")
        
        # Asserções
        self.assertTrue(valido, f"Comando deveria ser válido: {comando_esperado}")
        self.assertEqual(acao, acao_esperada, f"Ação incorreta. Esperado: {acao_esperada}, Obtido: {acao}")
        self.assertIn(dispositivo, dispositivo_esperado, f"Dispositivo incorreto. Esperado um de: {dispositivo_esperado}, Obtido: {dispositivo}")
        
        print("✓ Teste passou com sucesso!\n")
    
    def test_01_ligar_fonte_bancada(self):
        """Teste 1: Comando 'Ligar fonte de bancada'"""
        print("\n" + "="*70)
        print("TESTE 1: Ligar Fonte de Bancada")
        print("="*70)
        
        self._testar_comando_audio(
            arquivo_audio="ligar_fonte.wav",
            comando_esperado="Ligar fonte de bancada",
            acao_esperada="ligar",
            dispositivo_esperado=["fonte", "fonte de bancada", "bancada"]
        )
    
    def test_02_desligar_fonte_bancada(self):
        """Teste 2: Comando 'Desligar fonte de bancada'"""
        print("\n" + "="*70)
        print("TESTE 2: Desligar Fonte de Bancada")
        print("="*70)
        
        self._testar_comando_audio(
            arquivo_audio="desligar_fonte.wav",
            comando_esperado="Desligar fonte de bancada",
            acao_esperada="desligar",
            dispositivo_esperado=["fonte", "fonte de bancada", "bancada"]
        )
    
    def test_03_ligar_estacao_solda(self):
        """Teste 3: Comando 'Ligar estação de solda'"""
        print("\n" + "="*70)
        print("TESTE 3: Ligar Estação de Solda")
        print("="*70)
        
        self._testar_comando_audio(
            arquivo_audio="ligar_solda.wav",
            comando_esperado="Ligar estação de solda",
            acao_esperada="ligar",
            dispositivo_esperado=["solda", "estação", "estação de solda", "ferro"]
        )
    
    def test_04_desligar_estacao_solda(self):
        """Teste 4: Comando 'Desligar estação de solda'"""
        print("\n" + "="*70)
        print("TESTE 4: Desligar Estação de Solda")
        print("="*70)
        
        self._testar_comando_audio(
            arquivo_audio="desligar_solda.wav",
            comando_esperado="Desligar estação de solda",
            acao_esperada="desligar",
            dispositivo_esperado=["solda", "estação", "estação de solda", "ferro"]
        )
    
    def test_05_monitorar_energia(self):
        """Teste 5: Comando 'Monitorar energia consumida'"""
        print("\n" + "="*70)
        print("TESTE 5: Monitorar Energia Consumida")
        print("="*70)
        
        self._testar_comando_audio(
            arquivo_audio="monitorar_energia.wav",
            comando_esperado="Monitorar energia consumida",
            acao_esperada="monitorar",
            dispositivo_esperado=["energia", "consumo", "watts", "potência"]
        )
    
    def test_06_verificar_temperatura(self):
        """Teste 6: Comando 'Verificar temperatura dos equipamentos'"""
        print("\n" + "="*70)
        print("TESTE 6: Verificar Temperatura dos Equipamentos")
        print("="*70)
        
        self._testar_comando_audio(
            arquivo_audio="verificar_temperatura.wav",
            comando_esperado="Verificar temperatura dos equipamentos",
            acao_esperada="verificar",
            dispositivo_esperado=["temperatura", "calor", "equipamentos", "aquecimento"]
        )
    
    def test_07_registrar_tarefa(self):
        """Teste 7: Comando 'Registrar nova tarefa de reparo'"""
        print("\n" + "="*70)
        print("TESTE 7: Registrar Nova Tarefa de Reparo")
        print("="*70)
        
        self._testar_comando_audio(
            arquivo_audio="registrar_tarefa.wav",
            comando_esperado="Registrar nova tarefa de reparo",
            acao_esperada="registrar",
            dispositivo_esperado=["tarefa", "reparo", "manutenção", "registro", "log"]
        )
    
    def test_08_validacao_json_config(self):
        """Teste 8: Validar estrutura do arquivo JSON de configuração"""
        print("\n" + "="*70)
        print("TESTE 8: Validação do Arquivo de Configuração JSON")
        print("="*70)
        
        # Verifica se o arquivo existe
        self.assertTrue(os.path.exists(CONFIGURACOES), "Arquivo config.json não encontrado")
        print("✓ Arquivo config.json encontrado")
        
        # Verifica estrutura
        self.assertIn("acoes", self.acoes[0], "Estrutura JSON deve conter ações")
        print("✓ Estrutura de ações presente")
        
        # Verifica se tem pelo menos 4 tipos de ações diferentes
        acoes_unicas = set([acao["nome"] for acao in self.acoes])
        self.assertGreaterEqual(len(acoes_unicas), 4, "Deve haver pelo menos 4 tipos de ações")
        print(f"✓ Total de ações únicas configuradas: {len(acoes_unicas)}")
        
        # Lista todas as ações
        print("\nAções configuradas no JSON:")
        for i, acao in enumerate(acoes_unicas, 1):
            print(f"  {i}. {acao}")
        
        print("\n✓ Validação do JSON concluída com sucesso!")
    
    @classmethod
    def tearDownClass(cls):
        """Limpeza executada após todos os testes"""
        print("\n" + "="*70)
        print("TESTES CONCLUÍDOS")
        print("="*70)
        print("\nResumo:")
        print("✓ Todos os testes foram executados")
        print("✓ O assistente está pronto para uso")
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    # Cria o diretório de áudios se não existir
    if not os.path.exists(CAMINHO_AUDIOS):
        os.makedirs(CAMINHO_AUDIOS)
        print(f"Diretório de áudios criado: {CAMINHO_AUDIOS}")
        print("\n⚠️  ATENÇÃO: Você precisa gravar os seguintes arquivos de áudio:")
        print("  1. ligar_fonte.wav")
        print("  2. desligar_fonte.wav")
        print("  3. ligar_solda.wav")
        print("  4. desligar_solda.wav")
        print("  5. monitorar_energia.wav")
        print("  6. verificar_temperatura.wav")
        print("  7. registrar_tarefa.wav")
        print(f"\nSalve os áudios em: {CAMINHO_AUDIOS}\n")
    
    # Executa os testes
    unittest.main(verbosity=2)
