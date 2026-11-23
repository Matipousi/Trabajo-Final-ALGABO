# Guion del video (unos 20 minutos, 4 integrantes)

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Cada integrante se presenta con nombre y apellido al empezar su parte. Se muestra la pantalla con el informe,
el código o las figuras. Al final de cada parte, cada uno dice si usó IA en ella y para qué.

## Parte 1: Problema y datos (unos 5 min), Integrante 1
- El caso: un vehículo, un depósito, pedidos con cajas, prioridad y minutos de descarga. Hay que decidir qué pedidos, en qué orden y por qué tramos.
- Objetivo: máxima prioridad y, ante empate, menor tiempo. Restricciones: capacidad y límite de tiempo. Pasar por un centro no es atenderlo.
- Mostrar el caso chico de la guía (N00–N05–N09): completar la tabla en vivo y explicar por qué con 40 min conviene solo P06 y con 41, ambos.
- Datos: el dataset de la cátedra y los controles que se hicieron (`datos.py`). La pregunta del grupo y la adaptación: barrio nuevo, cierre de C25 y escenarios nuevos (`CAMBIOS.md`). Limitación: los datos son sintéticos.

## Parte 2: Los dos métodos (unos 6 min), Integrante 2
- Parte común: Dijkstra con heapq desde el depósito y desde cada centro. Por qué alcanza con caminos mínimos entre descargas.
- Referencia, el greedy: mostrar `referencia_greedy.py`. Rentabilidad = prioridad / minutos extra, inserción más barata, sin volver atrás. Garantía: factible. Límite: no es óptimo y no mira las cajas.
- Propuesta, la DP: mostrar `propuesta_dp.py`. Es la misma idea de la ADI 1 (Held–Karp): la celda (conjunto, último pedido) guarda el mínimo de viaje. Las dos podas (cajas y "volver directo") y por qué no descartan planes factibles. Garantía: óptimo. Límite: crece como 2ⁿ·n.

## Parte 3: Verificación y resultados (unos 6 min), Integrante 3
- Verificador independiente: recalcula desde `conexiones.csv`. Correr `python3 src/pruebas.py` en pantalla.
- Recalcular a mano el plan de la propuesta en E_BASE (67 + 29 = 96 min, 18 cajas, 79 puntos).
- Tabla de los 6 escenarios y figura 1: el greedy llena las cajas con pedidos cercanos y le sobra tiempo; la DP llega a P10.
- Cierres: el óptimo pierde como mucho 2 puntos y el greedy hasta 13 (C18).
- Red ampliada: el greedy repite el mismo plan; la DP aprovecha el barrio nuevo.
- Escalabilidad (figura 2): tiempo del programa ≠ minutos del plan. Ajustado: menos de 0,1 s con 24 pedidos. Holgado: unos 6 s con 24 pedidos. 3 semillas por tamaño; el greedy queda en promedio un 22–23 % por debajo del óptimo.

## Parte 4: Conclusiones e IA (unos 3 min), Integrante 4
- Recomendación: DP para este tamaño; el greedy solo si el problema es mucho más grande o hay que decidir al instante.
- Factibilidad ≠ optimalidad; no generalizar desde una instancia.
- Mejoras: un greedy que tenga en cuenta las cajas, búsqueda local o temple simulado, B&B con cota de mochila fraccionaria, AG.
- **Uso de IA:** se usó Claude Opus 5.5 para generar una versión completa de respaldo. Explicar qué partes se conservaron, cuáles se cambiaron y cómo se verificaron. Mostrar dónde están las evidencias (`DECLARACION_IA.md`, `evidencias_IA/`).
