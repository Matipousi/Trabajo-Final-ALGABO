# Declaración de uso de IA (sección 7 de la consigna)

## Uso 1: generación completa de la versión de respaldo

| Campo | Detalle |
|---|---|
| **Herramienta / modelo** | Claude Opus 5.5 (Anthropic), id `claude-opus-5-5`, usado mediante Claude Code (app de escritorio para Mac) |
| **Fecha** | 23/11/2026 (día del taller) |
| **Quién lo usó** | [Nombre del integrante] |
| **Finalidad concreta** | Tener una versión completa de respaldo ("piso") por si el grupo no llega a terminar o hay temas que no sabe implementar. El grupo trabaja después sobre esta base. |
| **Parte afectada** | **Todo** lo de esta carpeta: `src/*.py` (los 8 módulos), `datos/adaptados/` y `CAMBIOS.md`, `resultados/` (salidas de correr el código), `informe/informe.html` y `.pdf`, `README.md`, `guion_video.md` y este archivo. La pregunta del grupo, la elección de métodos (greedy vs. DP Held–Karp con poda), el diseño del barrio nuevo y de los escenarios también los propuso la IA. |
| **Evidencias** | Exportación completa de la conversación en `evidencias_IA/` (prompts y respuestas, con las salidas de cada ejecución). Cada `.py` tiene en el encabezado la marca `[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026]`. |

### Prompt principal (textual)
> "here you have the final assignment, can you check it for me? what's the rules about AI use in this? does it allow to code everything yourself?"
>
> "i want you to do everything, so i have a floor to stand on, once that's done, i'll start working on it myself with your assistance, this request is to have a fallback in case we don't finish the job in time or are topics we don't know how to implement here. in this version in which you'll do everything, say it, since it's mandatory to describe the use of ai"

### Qué hizo la IA (resumen de la sesión)
1. Leyó la consigna, la guía del taller y el `LEEME.md` del dataset.
2. Implementó la carga y validación, Dijkstra, el verificador independiente, el greedy y la DP.
3. Probó primero con los datos originales. Después cerró cada conexión de a una para ver dónde importa un cierre, y con eso eligió el escenario E_CIERRE (cierre de C25).
4. Diseñó el barrio nuevo (N16–N21, C30–C40, P11–P16) y los escenarios adaptados.
5. Escribió las pruebas: caso chico de la guía, fuerza bruta y planes inválidos. Al primer intento, el plan "pasa el límite de tiempo" fallaba también por capacidad, así que lo corrigió para que falle por la razón correcta.
6. Corrió los experimentos y escribió el informe con esos números.

### Verificaciones que hizo la IA (automáticas, reproducibles)
- `python3 src/pruebas.py`: todas pasan. Coinciden el caso chico calculado a mano, la DP contra la fuerza bruta en 4 escenarios y el rechazo de 6 planes inválidos.
- Todos los planes informados pasan por `verificador.py`, que recalcula los totales desde `conexiones.csv`.
- Recálculo a mano del plan de la propuesta en E_BASE, incluido en el informe (67 + 29 = 96 min, 18 cajas, prioridad 79).

## Intervención y verificación del grupo  ← COMPLETAR ANTES DE ENTREGAR
Para cada parte que se conserve, modifique o descarte, registrar:

| Parte | ¿Se incorporó, modificó o descartó? | Cómo lo verificamos (prueba, cálculo, fuente, comparación de versiones) | Quién |
|---|---|---|---|
| `propuesta_dp.py` | [ ] | [p. ej., traza a mano de la tabla con 3 pedidos] | [ ] |
| `referencia_greedy.py` | [ ] | [p. ej., primeras 2 elecciones de E_BASE calculadas a mano] | [ ] |
| `grafo.py` (Dijkstra) | [ ] | [ ] | [ ] |
| `verificador.py` | [ ] | [ ] | [ ] |
| Dataset adaptado | [ ] | [ ] | [ ] |
| Informe (cada sección) | [ ] | [ ] | [ ] |
| Video | [ ] | [ ] | [ ] |

## Usos posteriores
Agregar una tabla igual a la de arriba por cada nuevo uso de IA (herramienta, finalidad, parte, evidencia, verificación).
