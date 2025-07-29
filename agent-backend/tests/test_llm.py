import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from integracion_llm import LLMClient

class TestLLMClient(unittest.TestCase):
    def setUp(self):
        self.llm = LLMClient()

    def test_analizar_historia(self):
        historia = "Como usuario quiero poder iniciar sesión para acceder a mi perfil."
        resultado = self.llm.analizar_historia(historia)
        # El resultado puede variar según el modelo, pero debe ser un string no vacío
        self.assertIsInstance(resultado, str)
        self.assertTrue(len(resultado) > 0 or resultado is None)

if __name__ == "__main__":
    unittest.main()
