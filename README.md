# Trabajo final ALGABO: libros que tienen que llegar (VERSIÓN DE RESPALDO GENERADA POR IA)

> **Atención:** esta versión completa (datos adaptados, código, resultados, informe y guion) fue generada
> por **Claude Opus 5.5 (Anthropic) vía Claude Code el 23/11/2026**, a pedido de un integrante, como respaldo.
> Ver `DECLARACION_IA.md`. Antes de entregar, el grupo tiene que revisarla, verificarla y completar las partes
> marcadas como `[completar]`.

## Qué hace
Compara dos estrategias para decidir qué pedidos atender, en qué orden y por qué tramos viajar:
- **Referencia:** greedy de inserción (prioridad / minutos extra). Es rápida y factible, pero no garantiza el óptimo.
- **Propuesta:** programación dinámica Held–Karp sobre subconjuntos, con poda por capacidad y tiempo. Da el óptimo.

Ambas usan Dijkstra para calcular los caminos mínimos entre el depósito y los centros.

## Requisitos
- Python 3.10 o superior (probado con **Python 3.15.2**, macOS, Apple M5 Pro).
- **Sin dependencias externas**: solo biblioteca estándar (`csv`, `heapq`, `json`, `random`, `time`, `statistics`, `platform`).

## Cómo ejecutar (desde esta carpeta)
```bash
python3 src/preparar_datos.py
```
Regenera `datos/adaptados/` a partir de `datos/originales/`.
```bash
python3 src/pruebas.py
```
Corre el caso chico a mano, la fuerza bruta y los planes inválidos. Tarda menos de 1 s.
```bash
python3 src/experimentos.py
```
Corre la comparación completa y escribe en `resultados/`. Tarda unos 40 s.

Para el PDF del informe, se abre `informe/informe.html` en Chrome y se imprime como PDF (o con Chrome headless).
Todas las rutas son relativas a la carpeta del proyecto.

## Archivos
| Ruta | Contenido |
|---|---|
| `datos/originales/` | ZIP de la cátedra sin modificar (CSV, LEEME.md, generar_datos.py) |
| `datos/adaptados/` | Dataset adaptado (22 nodos, 40 conexiones, 16 pedidos, 6 escenarios) + `CAMBIOS.md` |
| `src/datos.py` | Carga y validación de los CSV |
| `src/grafo.py` | Lista de adyacencia, Dijkstra (heapq, entradas obsoletas), reconstrucción de caminos |
| `src/verificador.py` | Verificador independiente de factibilidad y totales, criterio de comparación |
| `src/referencia_greedy.py` | Solución de referencia (greedy de inserción) |
| `src/propuesta_dp.py` | Solución propuesta (Held–Karp con poda) |
| `src/preparar_datos.py` | Genera el dataset adaptado |
| `src/pruebas.py` | Verificación: caso chico, fuerza bruta, planes inválidos |
| `src/experimentos.py` | Programa principal: escenarios, cierres, escalabilidad, figuras |
| `src/figuras.py` | Figuras SVG (sin matplotlib) |
| `resultados/resultados.csv` | Tabla principal: plan, factibilidad, prioridad, cajas, viaje/servicio/total, ms, recorrido |
| `resultados/planes.json` | Planes completos (pedidos, orden, recorrido nodo por nodo, verificación) |
| `resultados/cierres.csv` | E_TIEMPO cerrando cada conexión de a una |
| `resultados/escalabilidad.csv` | Instancias aleatorias de 8 a 24 pedidos, semillas 1, 2 y 3 |
| `resultados/*.svg` | Figuras (red por escenario, escalabilidad) |
| `resultados/entorno.txt` | Versión de Python, sistema y procedimiento de medición |
| `informe/informe.html`, `informe/informe.pdf` | Informe |
| `guion_video.md` | Guion del video de unos 20 minutos, repartido en 4 partes |
| `DECLARACION_IA.md` | Declaración de uso de IA (obligatoria) |

## Semillas y reproducibilidad
- Los dos métodos son **deterministas**, con desempates explícitos: siempre dan el mismo plan.
- El azar solo aparece al generar las instancias de escalabilidad: semillas 1, 2 y 3, con `random.Random(semilla*1000 + n)`.
- Los tiempos de ejecución (ms) cambian según la máquina. Los planes y los minutos del plan no cambian.

## Atribución
Todo el código es original de esta versión, generado con IA (ver declaración). No se copió código de terceros.
Se usa solo la biblioteca estándar de Python. Los datos originales son de la cátedra ALGABO 2026 y son sintéticos.
