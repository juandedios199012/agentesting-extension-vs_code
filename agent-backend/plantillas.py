# plantillas.py
# Plantillas personalizables para generación de features y steps

PLANTILLAS = {
    "feature": {
        "es": "{feature}: {prompt}\n  {scenario}: {escenario}\n    {descripcion}\n    {given}\n    {when}\n    {then}\n",
        "en": "{feature}: {prompt}\n  {scenario}: {escenario}\n    {descripcion}\n    {given}\n    {when}\n    {then}\n"
    },
    "steps": {
        "es": "{given}\n{when}\n{then}\ndef {metodo}(context):\n    # Implementación del step\n    pass\n",
        "en": "{given}\n{when}\n{then}\ndef {metodo}(context):\n    # Step implementation\n    pass\n"
    }
}
