
"""
contextual_model.py
Entrena y ajusta el modelo LLM usando LangChain y el código fuente indexado.
"""


from config_azure_keyvault import cargar_secretos_keyvault
from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate



import pickle
import os


class ContextualModel:
    def __init__(self, index, model_path='context_model.pkl'):
        cargar_secretos_keyvault()  # Asegura que los secretos estén cargados antes de inicializar el modelo
        self.index = index
        self.llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")
        self.frameworks = ', '.join(index.get('frameworks', []))
        self.model_path = model_path
        self.training_data = []
        self._load_training_data()

    def _load_training_data(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.training_data = pickle.load(f)

    def _save_training_data(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.training_data, f)

    def train_on_workspace(self, new_examples=None):
        """
        Permite entrenar el agente con nuevos ejemplos/contexto del workspace.
        El usuario puede agregar ejemplos de prompts y respuestas para mejorar el modelo.
        """
        if new_examples:
            self.training_data.extend(new_examples)
            self._save_training_data()
        # Aquí podrías usar algoritmos ML/AI para ajustar el contexto, embeddings, etc.
        # Por ahora, se almacena el historial para enriquecer el contexto de los prompts.

    def generate_response(self, prompt):
        # Usa LangChain y el historial de entrenamiento para generar una respuesta contextual
        context_examples = '\n'.join([
            f"Prompt: {ex['prompt']}\nRespuesta: {ex['response']}" for ex in self.training_data[-5:]
        ])
        template = PromptTemplate(
            input_variables=["prompt", "frameworks", "context_examples"],
            template="""
Eres un agente experto en QA Automation. El proyecto usa los siguientes frameworks: {frameworks}.
Ejemplos previos de entrenamiento:
{context_examples}
Responde el siguiente prompt de forma contextual y específica al proyecto:
{prompt}
"""
        )
        final_prompt = template.format(prompt=prompt, frameworks=self.frameworks, context_examples=context_examples)
        return self.llm(final_prompt)

# Uso:
# model = ContextualModel(index)
# model.train_on_workspace([{'prompt': '...', 'response': '...'}])
# response = model.generate_response(prompt)
