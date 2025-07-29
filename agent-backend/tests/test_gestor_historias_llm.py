import unittest
import os
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gestor_historias import generar_artefactos_para_historias

class DummyLLM:
    def analizar_historia(self, historia_usuario):
        return "Feature: LLM\nScenario: LLM generado\nGiven ...\nWhen ...\nThen ..."

class TestGestorHistoriasLLM(unittest.TestCase):
    def setUp(self):
        self.carpeta_historias = "tests/historias"
        self.carpeta_salida = "tests/salida"
        os.makedirs(self.carpeta_historias, exist_ok=True)
        os.makedirs(self.carpeta_salida, exist_ok=True)
        with open(os.path.join(self.carpeta_historias, "historia1.txt"), "w", encoding="utf-8") as f:
            f.write("Como usuario quiero poder iniciar sesión para acceder a mi perfil.")

    def tearDown(self):
        for root, dirs, files in os.walk(self.carpeta_salida, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        for root, dirs, files in os.walk(self.carpeta_historias, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))

    def test_llm_integration(self):
        llm = DummyLLM()
        generar_artefactos_para_historias(self.carpeta_historias, self.carpeta_salida, llm=llm)
        archivos = os.listdir(self.carpeta_salida)
        self.assertTrue(any(a.endswith('_llm.txt') for a in archivos))

if __name__ == "__main__":
    unittest.main()
