import os
import json
a=""
prompt_db_vector = """Basado en los estándares ITU (específicamente ITU-T Y.1541 e ITU-T G.1010), necesito una distribución de ancho de banda para diferentes prioridades de casos de uso.
La información que proporciono es la siguiente:
    1. **Ancho de banda total disponible**: {total_bandwidth}.
    2. **Número de prioridades**: 3.
    3. **Número de usuarios por prioridad**:
        - Prioridad 1 (Alta): {p1_num}.
        - Prioridad 2 (Media): {p2_num}.
        - Prioridad 3 (Baja): {p3_num}.
Los casos de uso para cada prioridad son los siguientes:
    - **Prioridad 1 (Alta)**: Aplicaciones en tiempo real como VoIP y videoconferencias.
    - **Prioridad 2 (Media)**: Aplicaciones interactivas como streaming de video y teletrabajo
    - **Prioridad 3 (Baja)**: Aplicaciones no críticas como navegación web y descargas.Basado en los estándares ITU,
    ¿cuál sería la distribución óptima de ancho de banda para cada prioridad, considerando el ancho de banda total, el número de prioridades y la
    cantidad de usuarios por prioridad? Proporciona una explicación clara de cómo se calcula la distribución y justifica los porcentajes asignados a cada prioridad.
""".format_map({"total_bandwidth":a, "p1_num":"", "p2_num":"", "p3_num":""})



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
    **Cálculo de la Distribución**:- **Ancho de banda total**: [Inserte el valor en Mbps/Gbps].
    - **Ancho de banda para Prioridad 1**: 40% del total.
    - **Ancho de banda para Prioridad 2**: 35% del total.
    - **Ancho de banda para Prioridad 3**: 25% del total.
Esta distribución asegura que las aplicaciones críticas reciban el ancho de banda necesario mientras se optimiza el uso de los recursos disponibles.
"""
