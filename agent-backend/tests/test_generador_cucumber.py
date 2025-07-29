import unittest
from generador_cucumber import GeneradorCucumber

class TestGeneradorCucumber(unittest.TestCase):
    def setUp(self):
        self.conocimiento = {
            'descripciones': [{'metodo': 'Login', 'descripcion': 'Como usuario quiero iniciar sesión.'}],
            'metodos_test': ['Login']
        }
        self.generador = GeneradorCucumber(self.conocimiento)

    def test_feature_es(self):
        from config import CONFIG
        CONFIG['IDIOMA'] = 'es'
        features = self.generador.generar_feature('Login')
        self.assertTrue(any('Feature' in f for f in features))
        self.assertTrue(any('Given el sistema está en estado inicial' in f for f in features))

    def test_feature_en(self):
        from config import CONFIG
        CONFIG['IDIOMA'] = 'en'
        features = self.generador.generar_feature('Login')
        self.assertTrue(any('Feature' in f for f in features))
        self.assertTrue(any('Given the system is in initial state' in f for f in features))

    def test_steps_es(self):
        from config import CONFIG
        CONFIG['IDIOMA'] = 'es'
        steps = self.generador.generar_step_definitions('Login')
        self.assertTrue(any('@Given' in s for s in steps))
        self.assertTrue(any('def Login' in s for s in steps))

    def test_steps_en(self):
        from config import CONFIG
        CONFIG['IDIOMA'] = 'en'
        steps = self.generador.generar_step_definitions('Login')
        self.assertTrue(any('@Given' in s for s in steps))
        self.assertTrue(any('def Login' in s for s in steps))

if __name__ == '__main__':
    unittest.main()
