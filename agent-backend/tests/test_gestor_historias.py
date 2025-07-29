import unittest
from gestor_historias import cargar_historias

class TestGestorHistorias(unittest.TestCase):
    def test_cargar_historias_vacia(self):
        historias = cargar_historias('tests/recursos_vacia')
        self.assertEqual(historias, [])

    def test_cargar_historias_mock(self):
        import os
        carpeta = 'tests/recursos_mock'
        os.makedirs(carpeta, exist_ok=True)
        with open(f'{carpeta}/HistoriaMock.txt', 'w', encoding='utf-8') as f:
            f.write('Como usuario quiero probar el gestor.')
        historias = cargar_historias(carpeta)
        self.assertTrue(any(h['nombre'] == 'HistoriaMock.txt' for h in historias))
        os.remove(f'{carpeta}/HistoriaMock.txt')
        os.rmdir(carpeta)

if __name__ == '__main__':
    unittest.main()
