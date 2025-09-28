# PreFlopData
Problema a resolver:
El análisis de torneos de póker es complicado porque los registros de manos, rondas y apuestas no suelen estar disponibles en un formato estructurado ni visualizable, dificultando la identificación de patrones de juego, evaluación de estrategias y comprensión de tendencias.

Usuarios afectados:
- Jugadores de póker que desean mejorar sus estrategias.
- Analistas de datos y entusiastas de EDA aplicados a juegos de azar.

Necesidad actual:
- No existen herramientas accesibles que permitan explorar, filtrar y visualizar datos de torneos de póker de forma intuitiva.

Objetivo principal:
- Construir una aplicación web que permita explorar un datasets de póker mediante estadísticas, visualizaciones y detección de patrones, de manera amigable a los usuarios.

Alcances:
- Generar un dataset simulado de póker con miles de manos.
- Permitir carga y exploración del dataset en la web.
- Mostrar estadísticas descriptivas (botes promedio, frecuencia de rondas, acciones más comunes).
- Detectar patrones básicos de apuestas y resultados.

Fuera de alcance:
- Conexión con datos reales.
- Modelos predictivos avanzados.
- Simulación en tiempo real de partidas.

Selección del paradigma de programación

Paradigmas seleccionados:
- POO (Programación Orientada a Objetos): Para modelar entidades como Mano, Mesa, Ronda y Torneo, con atributos y métodos.
- Programación Funcional: Para el cálculo de estadísticas agregadas (promedios, tasas, frecuencias).
- Programación Estructurada: Para el flujo principal del sistema (lectura de datos, carga en memoria, ejecución de funciones).

Justificación:
- La combinación de POO y funciones puras permite organizar mejor los datos de torneos y realizar cálculos estadísticos de manera modular y reusable.

Dataset seleccionado

- Tipo: Simulado.
- Origen: Script en Python que genera manos de póker con rondas, apuestas y ganadores.
- Tamaño: 1.000 manos inicial, escalable a decenas de miles.

Licencia: Creative Commons Zero (CC0).

Diccionario de datos:

Campo       |  Tipo    |  Descripción                                              
------------+----------+-----------------------------------------------------------

mano_id     |  int     |  Identificador único de la mano                           
mesa        |  int     |  Número de la mesa donde se jugó la mano                  
ronda       |  string  |  Etapa de la mano (Preflop, Flop, Turn, River, Showdown)  
apuestas    |  string  |  Secuencia de acciones realizadas en la ronda             
bote_final  |  int     |  Total de fichas acumuladas en el bote                    
ganador     |  string  |  Identificador del jugador ganador (Jugador_1 … Jugador_9)

Diagrama de arquitectura

Componentes principales:
- Frontend (interfaz web): Permite la carga y visualización del dataset, filtrado y estadísticas.
- Backend (Flask en Python): Procesa la lógica de negocio y genera estadísticas, visualizaciones y patrones básicos.
- Base de datos/archivos: Almacena los datasets cargados y generados. Puede utilizar almacenamiento temporal (archivos locales) para la fase inicial.

Diagrama de referencia (basado en el esquema entregado):
- Incluye la interacción del cliente desde la web (exploración/carga de datos), la comunicación entre frontend y backend vía HTTP/REST, y la separación lógica de procesamiento (backend) y almacenamiento (data).
