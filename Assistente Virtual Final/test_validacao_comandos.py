import unittest
import json
import unittest
import json
import unittest
import json
import ast

# Import dependencies for the extracted function
from fuzzy_match import corrigir_acao, corrigir_dispositivo

# Extract validar_comando function from assistente.py using AST
with open("assistente.py", "r", encoding="utf-8") as f:
    content = f.read()

tree = ast.parse(content)
function_node = None
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "validar_comando":
        function_node = node
        break

if not function_node:
    raise Exception("Could not find validar_comando function in assistente.py")

# Compile and execute the function definition
# We wrap it in a Module to compile it
module = ast.Module(body=[function_node], type_ignores=[])
code = compile(module, filename="<ast>", mode="exec")
exec(code)

# Now validar_comando is defined in this scope


# Mock configuration for testing
MOCK_CONFIG = {
    "acoes": [
        {
            "nome": "ligar",
            "sinonimos": ["ativar", "acionar"],
            "dispositivos": ["fonte", "fonte de bancada", "solda", "estação de solda"]
        },
        {
            "nome": "desligar",
            "sinonimos": ["desativar", "parar"],
            "dispositivos": ["fonte", "fonte de bancada", "solda", "estação de solda"]
        },
        {
            "nome": "monitorar",
            "sinonimos": ["acompanhar", "ver", "checar"],
            "dispositivos": ["energia", "energia consumida", "consumo", "consumida"]
        },
        {
            "nome": "verificar",
            "sinonimos": ["checar", "ler", "medir"],
            "dispositivos": ["temperatura", "temperatura equipamentos", "equipamentos"]
        },
        {
            "nome": "registrar",
            "sinonimos": ["anotar", "salvar", "iniciar", "nova", "novo", "criar"],
            "dispositivos": ["tarefa", "reparo", "manutenção"]
        }
    ]
}

class TestValidacaoComandos(unittest.TestCase):
    
    def test_comando_exato(self):
        comando = ["ligar", "fonte"]
        valido, acao, dispositivo = validar_comando(comando, MOCK_CONFIG["acoes"])
        self.assertTrue(valido)
        self.assertEqual(acao, "ligar")
        self.assertEqual(dispositivo, "fonte")

    def test_sinonimo_acao(self):
        # "ativar fonte" -> deve mapear para "ligar"
        comando = ["ativar", "fonte"]
        valido, acao, dispositivo = validar_comando(comando, MOCK_CONFIG["acoes"])
        self.assertTrue(valido)
        self.assertEqual(acao, "ligar")
        self.assertEqual(dispositivo, "fonte")

    def test_sinonimo_registro(self):
        # "nova tarefa" -> deve mapear para "registrar"
        comando = ["nova", "tarefa"]
        valido, acao, dispositivo = validar_comando(comando, MOCK_CONFIG["acoes"])
        self.assertTrue(valido)
        self.assertEqual(acao, "registrar")
        self.assertEqual(dispositivo, "tarefa")

    def test_sinonimo_registro_iniciar_reparo(self):
        # "iniciar reparo" -> deve mapear para "registrar"
        comando = ["iniciar", "reparo"]
        valido, acao, dispositivo = validar_comando(comando, MOCK_CONFIG["acoes"])
        self.assertTrue(valido)
        self.assertEqual(acao, "registrar")
        self.assertEqual(dispositivo, "reparo")

    def test_fuzzy_dispositivo(self):
        # "ligar font" (typo) -> deve corrigir para "fonte"
        comando = ["ligar", "font"]
        valido, acao, dispositivo = validar_comando(comando, MOCK_CONFIG["acoes"])
        self.assertTrue(valido)
        self.assertEqual(acao, "ligar")
        self.assertEqual(dispositivo, "fonte")

    def test_fuzzy_acao_e_dispositivo(self):
        # "liga font" (typo em ambos) -> deve corrigir
        comando = ["liga", "font"]
        valido, acao, dispositivo = validar_comando(comando, MOCK_CONFIG["acoes"])
        self.assertTrue(valido)
        self.assertEqual(acao, "ligar")
        self.assertEqual(dispositivo, "fonte")

    def test_comando_invalido(self):
        comando = ["fazer", "cafe"]
        valido, acao, dispositivo = validar_comando(comando, MOCK_CONFIG["acoes"])
        self.assertFalse(valido)

if __name__ == '__main__':
    unittest.main()
