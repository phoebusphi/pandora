import os
import json
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone as pinelang
from langchain.vectorstores.utils import DistanceStrategy

load_dotenv()

os.environ["OPENAI_API_TYPE"] = "openai"
os.environ["MODEL_OPENAI_4O"] = "gpt-4o"
os.environ["OPENAI_API_KEY"] = ""
os.environ['PINECONE_API_KEY'] = ""

# prompt_db_vector = """Basado en los estándares ITU (específicamente ITU-T Y.1541 e ITU-T G.1010), necesito una distribución de ancho de banda para diferentes prioridades de casos de uso.
# La información que proporciono es la siguiente:
#     1. **Ancho de banda total disponible**: {total_bandwidth}.
#     2. **Número de prioridades**: 3.
#     3. **Número de usuarios por prioridad**:
#         - Prioridad 1 (Alta): {p1_num}.
#         - Prioridad 2 (Media): {p2_num}.
#         - Prioridad 3 (Baja): {p3_num}.
# Los casos de uso para cada prioridad son los siguientes:
#     - **Prioridad 1 (Alta)**: Aplicaciones en tiempo real como VoIP y videoconferencias.
#     - **Prioridad 2 (Media)**: Aplicaciones interactivas como streaming de video y teletrabajo
#     - **Prioridad 3 (Baja)**: Aplicaciones no críticas como navegación web y descargas.Basado en los estándares ITU,
#     ¿cuál sería la distribución óptima de ancho de banda para cada prioridad, considerando el ancho de banda total, el número de prioridades y la
#     cantidad de usuarios por prioridad? Proporciona una explicación clara de cómo se calcula la distribución y justifica los porcentajes asignados a cada prioridad.
# """
prompt_db_vector="""
Based on ITU standards (specifically ITU-T Y.1541 and ITU-T G.1010), I need a bandwidth distribution for different use case priorities.
The information provided is as follows:
1. Total available bandwidth: {total_bandwidth}.
2. Number of priorities: 3.
3. Number of users per priority:
- Priority 1 (High): {p1_num}.
- Priority 2 (Medium): {p2_num}.
- Priority 3 (Low): {p3_num}.
The use cases for each priority are as follows:
- Priority 1 (High): Real-time applications like VoIP and video conferencing.
- Priority 2 (Medium): Interactive applications like video streaming and telework.
- Priority 3 (Low): Non-critical applications like web browsing and downloads.
Based on ITU standards, what would be the optimal bandwidth distribution for each priority, considering the total bandwidth, number of priorities, and number of users per priority? Provide a clear explanation of how the distribution is calculated and justify the percentages assigned to each priority.
"""


answere = """
Basado en los estándares ITU-T Y.1541 e ITU-T G.1010, la distribución de ancho de banda para las prioridades dadas sería la siguiente:
    1. **Prioridad 1 (Alta) - VoIP y Videoconferencias**:
        - **Porcentaje de ancho de banda**: 40%.
        - **Justificación**: Las aplicaciones en tiempo real requieren baja latencia y un ancho de banda garantizado para asegurar una calidad de servicio (QoS) óptima. Según ITU-T Y.1541, el tráfico en tiempo real debe tener la máxima prioridad.
    2. **Prioridad 2 (Media) - Streaming y Teletrabajo**:
        - **Porcentaje de ancho de banda**: 35%.
        - **Justificación**: Las aplicaciones interactivas necesitan un ancho de banda suficiente para evitar buffering y retrasos, pero no requieren la misma prioridad que las aplicaciones en tiempo real. ITU-T G.1010 recomienda asignar un ancho de banda moderado para este tipo de tráfico.
    3. **Prioridad 3 (Baja) - Navegación Web y Descargas**:
        - **Porcentaje de ancho de banda**: 25%.
        - **Justificación**: Las aplicaciones no críticas pueden funcionar con un ancho de banda limitado sin afectar significativamente la experiencia del usuario. Este tipo de tráfico tiene la menor prioridad según los estándares ITU.
    **Cálculo de la Distribución**:- **Ancho de banda total**: {response}.
    - **Ancho de banda para Prioridad 1**: 40% del total.
    - **Ancho de banda para Prioridad 2**: 35% del total.
    - **Ancho de banda para Prioridad 3**: 25% del total.
Esta distribución asegura que las aplicaciones críticas reciban el ancho de banda necesario mientras se optimiza el uso de los recursos disponibles.
"""

# complement_info = """
# Eres un experto en redes con amplia experiencia en análisis de latencia y rendimiento de sistemas de comunicación. Tu objetivo es proporcionar una respuesta que integre dos fuentes de información:

# 1. Base de conocimiento: Explicación técnica de la latencia promedio en una red, incluyendo factores que la influyen y su importancia en el rendimiento de sistemas de comunicación.

# 2. Algoritmo genético: Análisis de la latencia promedio de una población de redes, utilizando técnicas de selección, cruce y mutación para optimizar los parámetros de latencia.

# Elabora una respuesta que:
# - Explique detalladamente el concepto de latencia desde la base de conocimiento
# - Describa cómo el algoritmo genético puede modelar y optimizar la latencia promedio
# - Integre los resultados del algoritmo genético con la explicación teórica de la base de conocimiento
# - Proporcione insights sobre cómo mejorar la latencia en diferentes escenarios de red

# Prioriza la claridad en la explicación, mostrando cómo las dos fuentes de información {conocimiento} y la latencia obtenida del algoritmo genetico es la
# siguiente {latencia} se complementan para ofrecer una comprensión más profunda de la latencia en redes.
# """


embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

def improve_response(original_response:str,pos, latency,bw_total):
    apikey = os.environ["OPENAI_API_KEY"]

    complement_info= """
    You are a network expert with extensive experience in latency analysis and communication system performance. Your goal is to provide a response that integrates two sources of information:
    1. Knowledge base: Technical explanation of average network latency, including factors that influence it and its importance in communication system performance.
    2. Genetic algorithm: Analysis of average latency of a network population, using selection, crossover, and mutation techniques to optimize latency parameters.
    Develop a response that:
    - Explains the concept of latency in detail from the knowledge base
    - Describes how the genetic algorithm can model and optimize average latency
    - Integrates the genetic algorithm results with the theoretical explanation from the knowledge base
    - Provides insights on how to improve latency in different network scenarios

    Prioritize clarity in the explanation, showing how the two information sources {conocimiento} and the latency obtained from the genetic algorithm {latencia} complement each other to offer a deeper understanding of network latency. The router location found by the genetic algorithm was the following {position} in latitude and longitude.

    Use the following information to complement the response:
    Based on ITU-T Y.1541 and ITU-T G.1010 standards, the bandwidth distribution for the given priorities would be as follows:
        1. **Priority 1 (High) - VoIP and Video Conferencing**:
            - **Bandwidth percentage**: 40%.
            - **Justification**: Real-time applications require low latency and guaranteed bandwidth to ensure optimal quality of service (QoS). According to ITU-T Y.1541, real-time traffic must have the highest priority.
        2. **Priority 2 (Medium) - Streaming and Telework**:
            - **Bandwidth percentage**: 35%.
            - **Justification**: Interactive applications need sufficient bandwidth to avoid buffering and delays, but do not require the same priority as real-time applications. ITU-T G.1010 recommends allocating moderate bandwidth for this type of traffic.
        3. **Priority 3 (Low) - Web Browsing and Downloads**:
            - **Bandwidth percentage**: 25%.
            - **Justification**: Non-critical applications can function with limited bandwidth without significantly affecting user experience. This type of traffic has the lowest priority according to ITU standards.
        **Distribution Calculation**:
        - **Total Bandwidth**: {bandwidth}.
        - **Bandwidth for Priority 1**: 40% of total.
        - **Bandwidth for Priority 2**: 35% of total.
        - **Bandwidth for Priority 3**: 25% of total.
    This distribution ensures that critical applications receive the necessary bandwidth while optimizing the use of available resources.
    """.format_map({"conocimiento":original_response, "latencia":"{} ms".format(latency), "position":str(pos), "bandwidth":"{} Giga bits".format(bw_total)  })

    llm = ChatOpenAI(model="gpt-4o",temperature=0.16,api_key=apikey,)
    chain = llm.invoke(complement_info)
    return chain


def consult_db(question,pos, latency, bw_total):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "hackathon"
    index = pc.Index(index_name)
    vectorstore = pinelang(index, embeddings_model.embed_query,"text",
                                        distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE)
    response = vectorstore.similarity_search(question,
                                            namespace="connectivity", k=10)
    improved_response = improve_response(response[0].page_content,pos, latency,bw_total)
    return improved_response.content
