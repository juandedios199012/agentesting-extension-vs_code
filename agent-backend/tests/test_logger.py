import unittest
from logger import log_event

class TestLogger(unittest.TestCase):
    def test_log_event_info(self):
        try:
            log_event("Mensaje de prueba INFO", "INFO")
        except Exception as e:
            self.fail(f"log_event lanzó una excepción: {e}")

    def test_log_event_error(self):
        try:
            log_event("Mensaje de prueba ERROR", "ERROR")
        except Exception as e:
            self.fail(f"log_event lanzó una excepción: {e}")

if __name__ == '__main__':
    unittest.main()
