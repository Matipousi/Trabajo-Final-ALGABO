# Registro de cambios del dataset adaptado

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Esta carpeta la genera `src/preparar_datos.py` a partir de `datos/originales/`, que no se modifica.
**Todos los datos agregados son sintéticos**: fueron inventados para el estudio, igual que el paquete original.

**Pregunta que motiva la adaptación:** ¿cuándo conviene el método exacto (DP) y cuándo alcanza con el greedy?
¿Cambia la respuesta si se cierra un tramo con el tiempo ajustado, o si la red crece con un barrio nuevo y más lejano?

| Archivo | Cambio | Motivo |
|---|---|---|
| nodos.csv | + N16–N21 (centros 11–16), en x=4 (este) e y=4 (norte) | Barrio nuevo, más lejos del depósito |
| conexiones.csv | + C30–C40, de 5 a 8 min | Conectar el barrio con tiempos dentro del rango original (5–10) |
| pedidos.csv | + P11–P16, uno por centro nuevo (2–6 cajas, prioridad 9–25, servicio 4–9) | Más opciones, en el mismo rango que los originales |
| escenarios.csv | + columnas `pedidos_incluidos` y `conexiones_cerradas` | Elegir pedidos y cierres por escenario |
| escenarios.csv | + E_CIERRE (E_TIEMPO sin C25 N00–N05) | Robustez ante el cierre de una salida del depósito |
| escenarios.csv | + E_AMPLIADO (16 pedidos, 24 cajas, 160 min) | Problema más grande con más recursos |
| escenarios.csv | + E_AMPLIADO_BASE (16 pedidos, 18 cajas, 130 min) | Igual que E_BASE, cambiando solo la cantidad de pedidos |

Los escenarios E_BASE, E_CAPACIDAD y E_TIEMPO se conservan idénticos (P01–P10, sin cierres), como control.

**Controles ejecutados** (`datos.validar_datos`): ids únicos, tipos válidos, un depósito, extremos existentes,
tiempos positivos, sin duplicados ni lazos, pedidos en centros existentes (uno por centro), referencias de
escenarios válidas y alcanzabilidad desde el depósito. Resultado: 0 problemas.

**Limitaciones:** son datos inventados; los valores del barrio nuevo se eligieron a mano, dentro de los rangos del original.
