# Cargar el índice desde el almacenamiento (si lo guardaste)
from llama_index.core import StorageContext, load_index_from_storage
storage_context = StorageContext.from_defaults(persist_dir='index_storage')
index = load_index_from_storage(storage_context)

# Crear un motor de consulta y hacer preguntas
query_engine = index.as_query_engine()
response = query_engine.query("¿Qué podrías decirme como resumen?")
print(response)
