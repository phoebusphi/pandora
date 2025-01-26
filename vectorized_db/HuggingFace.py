from transformers import AutoTokenizer, AutoModel
from llama_index.core.embeddings import BaseEmbedding
from pydantic import PrivateAttr
import torch


class HuggingFaceEmbedding(BaseEmbedding):
    # Atributos privados para que Pydantic no los valide
    _tokenizer: AutoTokenizer = PrivateAttr()
    _model: AutoModel = PrivateAttr()

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", **kwargs):
        super().__init__(**kwargs)  # Inicializar la clase base
        # Cargar el modelo y el tokenizador desde Hugging Face
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModel.from_pretrained(model_name)

    def _get_query_embedding(self, query: str):
        # Generar embedding para una consulta
        inputs = self._tokenizer(query, return_tensors="pt", padding=True, truncation=True)
        outputs = self._model(**inputs)
        # Promediar las representaciones de los tokens para obtener un solo vector
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
        return embedding

    def _get_text_embedding(self, text: str):
        # Generar embedding para un texto
        return self._get_query_embedding(text)

    async def _aget_query_embedding(self, query: str):
        # Implementación asíncrona del método
        return self._get_query_embedding(query)