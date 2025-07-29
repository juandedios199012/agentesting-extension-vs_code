# main.py
# Archivo inicial para el agente Python


def main():
    print("Agente Python iniciado correctamente.")
    from gestor_historias import generar_artefactos_para_historias

    ruta_historias = "E:/Cursos/DiplomadoTesting-Bolivia/Proyecto-Final-Diplomado-Software-Testing_v3/FlexBusinessMobile-test-ui-with-ai/src/test/resources"
    ruta_salida = "E:/Cursos/DiplomadoTesting-Bolivia/Proyecto-Final-Diplomado-Software-Testing_v3/FlexBusinessMobile-test-ui-with-ai/src/test/generated"

    # Crear carpeta de salida si no existe
    import os
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    generar_artefactos_para_historias(ruta_historias, ruta_salida)
    print(f"\nArtefactos generados en: {ruta_salida}")

if __name__ == "__main__":
    main()
