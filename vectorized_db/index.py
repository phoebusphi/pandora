from llama_index.core import SimpleDirectoryReader
from llama_index.core import GPTVectorStoreIndex
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from HuggingFace import HuggingFaceEmbedding

# Leer todos los archivos PDF en la carpeta '../documentation'
documents = SimpleDirectoryReader('../documentation').load_data()

# Verificar que los documentos se hayan cargado
print(documents[0].text[:500])  # Muestra los primeros 500 caracteres del primer documento

# Crear el modelo de embeddings basado en Hugging Face
embedding_model = HuggingFaceEmbedding()

# Crear el índice usando los documentos y el modelo de embeddings personalizado
index = GPTVectorStoreIndex.from_documents(
    documents,
    embed_model=embedding_model
)

# Guardar el índice en almacenamiento local (opcional)
index.storage_context.persist('index_storage')


