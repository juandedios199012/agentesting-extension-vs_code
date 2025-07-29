# generador_cucumber.py
# Módulo para generar archivos feature y step definitions en Cucumber


from logger import log_event
from config import CONFIG
from plantillas import PLANTILLAS

class GeneradorCucumber:
    def __init__(self, conocimiento):
        self.conocimiento = conocimiento

    def generar_feature(self, prompt):
        log_event(f"Generando archivo feature para: {prompt}", "INFO")
        idioma = CONFIG.get("IDIOMA", "es")
        plantilla = PLANTILLAS["feature"].get(idioma, PLANTILLAS["feature"]["es"])
        palabras = {
            "es": {
                "feature": "Feature",
                "scenario": "Scenario",
                "given": "Given el sistema está en estado inicial",
                "when": "When el usuario realiza la acción principal",
                "then": "Then se valida el resultado esperado"
            },
            "en": {
                "feature": "Feature",
                "scenario": "Scenario",
                "given": "Given the system is in initial state",
                "when": "When the user performs the main action",
                "then": "Then the expected result is validated"
            }
        }
        p = palabras.get(idioma, palabras["es"])
        features = []
        for desc in self.conocimiento.get('descripciones', []):
            feature = plantilla.format(
                feature=p['feature'],
                prompt=prompt,
                scenario=p['scenario'],
                escenario=desc['metodo'].replace('_', ' '),
                descripcion=desc['descripcion'].strip(),
                given=p['given'],
                when=p['when'],
                then=p['then']
            )
            features.append(feature)
        log_event(f"Archivo feature generado para: {prompt}", "INFO")
        return features

    def generar_step_definitions(self, prompt):
        log_event(f"Generando step definitions para: {prompt}", "INFO")
        idioma = CONFIG.get("IDIOMA", "es")
        plantilla = PLANTILLAS["steps"].get(idioma, PLANTILLAS["steps"]["es"])
        palabras = {
            "es": {
                "given": "@Given('el sistema está en estado inicial')",
                "when": "@When('el usuario realiza la acción principal')",
                "then": "@Then('se valida el resultado esperado')"
            },
            "en": {
                "given": "@Given('the system is in initial state')",
                "when": "@When('the user performs the main action')",
                "then": "@Then('the expected result is validated')"
            }
        }
        p = palabras.get(idioma, palabras["es"])
        steps = []
        for metodo in self.conocimiento.get('metodos_test', []):
            step_def = plantilla.format(
                given=p['given'],
                when=p['when'],
                then=p['then'],
                metodo=metodo
            )
            steps.append(step_def)
        log_event(f"Archivo step definitions generado para: {prompt}", "INFO")
        return steps
