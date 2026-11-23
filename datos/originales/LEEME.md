# Datos sintéticos: entregas a bibliotecas comunitarias

Documentación versión 1.1. Datos de referencia versión 1.0. Curso ALGABO, 2026.

## Procedencia y propósito

Todos los datos de este paquete fueron creados para un caso académico ficticio. Ninguna persona, biblioteca, dirección, calle o lugar real está representado. Los nombres «Depósito», «Centro» y «Cruce» son etiquetas genéricas. Los tiempos, las cantidades y las prioridades son valores sintéticos; no proceden de observaciones ni de un servicio real.

Un vehículo sale del depósito con lotes de libros, atiende un subconjunto de pedidos de centros comunitarios y regresa al mismo depósito. La red tiene 16 nodos y 29 conexiones; hay 10 pedidos, cada uno en un centro diferente. Los tres escenarios utilizan exactamente la misma red y los mismos pedidos: cambian únicamente las restricciones indicadas en `escenarios.csv`.

## Uso en el trabajo final

Este dataset es un punto de partida para comprender el caso y probar soluciones. Para el trabajo final, cada grupo debe **adaptarlo de forma justificada o utilizar otro dataset**. Puede ampliar la red, incorporar pedidos o construir escenarios propios que permitan analizar una situación nueva. Cambiar nombres o números sin explicar qué se busca estudiar no es una adaptación suficiente.

Buscar otro dataset es una alternativa, no una obligación. El informe debe justificar la elección, explicar cambios y preparación, y documentar fuentes, calidad, limitaciones y datos sintéticos. No se valora el tamaño ni la procedencia real por sí solos. Comparen las dos soluciones en al menos tres escenarios del dataset final; si parten del ejemplo, al menos uno debe permitir evaluar la adaptación. Usar íntegramente el dataset original, sin adaptación justificada, no cumple la consigna. La adaptación puede estar en la red o los pedidos: no es obligatorio cambiar también los límites de los escenarios.

## Archivos y lectura

- `nodos.csv`: identificadores, tipos y posiciones abstractas de los nodos.
- `conexiones.csv`: conexiones de la red y minutos de viaje en cada una.
- `pedidos.csv`: cajas, prioridad y minutos de servicio de cada pedido.
- `escenarios.csv`: depósito y límites de carga y tiempo de cada escenario.
- `generar_datos.py`: reproduce exactamente los cuatro CSV publicados.
- `LEEME.md`: significado de los campos y reglas del caso.

Los CSV usan UTF-8 sin BOM, coma como separador, una fila inicial de cabeceras y salto de línea LF. Las cabeceras son ASCII. Los decimales se escriben con punto; no hay separadores de miles ni valores vacíos. Cajas, prioridades y tiempos son enteros; las coordenadas tienen una cifra decimal. Las filas no expresan un orden de visita. Los identificadores son texto y deben conservarse completos, incluidos los ceros iniciales.

## Diccionario completo

### `nodos.csv`

| Campo | Tipo y unidad | Significado |
|---|---|---|
| `nodo_id` | Texto, clave única | Identificador estable `N00` a `N15`. |
| `tipo` | Texto | Uno de `deposito`, `centro`, `interseccion`. Hay un depósito, diez centros y cinco intersecciones. |
| `nombre` | Texto | Etiqueta ficticia para identificar el nodo al presentar resultados. |
| `x` | Decimal, unidad abstracta | Coordenada horizontal para dibujar la red. |
| `y` | Decimal, unidad abstracta | Coordenada vertical para dibujar la red. |

Las coordenadas no son geográficas, no se miden en kilómetros y no determinan el tiempo de viaje. Los costos que se deben utilizar son los valores de `tiempo_min` de las conexiones. Que dos posiciones estén próximas en el dibujo no crea una conexión. Si dos segmentos se cruzan en un dibujo, ese cruce no permite cambiar de conexión salvo que compartan un `nodo_id` en sus extremos.

### `conexiones.csv`

| Campo | Tipo y unidad | Significado |
|---|---|---|
| `conexion_id` | Texto, clave única | Identificador estable `C01` a `C29`. |
| `origen` | Texto, referencia a `nodos.nodo_id` | Uno de los extremos de la conexión. |
| `destino` | Texto, referencia a `nodos.nodo_id` | El otro extremo de la conexión. |
| `tiempo_min` | Entero positivo, minutos | Tiempo de recorrer esta conexión en cualquiera de los dos sentidos. |

La red es **no dirigida**. Cada conexión se registra una sola vez: `origen` y `destino` son nombres de columnas, no una restricción de sentido. No hay lazos ni pares de extremos repetidos. Solo se puede pasar directamente entre nodos unidos por una conexión publicada. Los tiempos son fijos y se suman cada vez que se recorre una conexión, incluso si ya fue recorrida. La red es conexa.

### `pedidos.csv`

| Campo | Tipo y unidad | Significado |
|---|---|---|
| `pedido_id` | Texto, clave única | Identificador estable `P01` a `P10`. |
| `nodo_id` | Texto, referencia a `nodos.nodo_id` | Centro en el que se atiende el pedido; es único entre pedidos. |
| `cajas` | Entero positivo, cajas | Carga indivisible requerida por el pedido completo. |
| `prioridad` | Entero positivo, puntos | Aporte al objetivo si el pedido completo es atendido. No es dinero ni prioridad por caja. |
| `servicio_min` | Entero positivo, minutos | Tiempo fijo para completar la entrega del pedido, además del viaje. |

Un pedido se atiende completo o no se atiende. No hay entregas parciales ni un aporte proporcional de prioridad. Cada pedido puede aportar prioridad una sola vez y requiere su tiempo de servicio una sola vez. Todos los lotes de los pedidos elegidos se cargan al inicio; no hay recargas ni recogidas durante el recorrido. La carga inicial es la suma de `cajas` de los pedidos elegidos.

### `escenarios.csv`

| Campo | Tipo y unidad | Significado |
|---|---|---|
| `escenario_id` | Texto, clave única | Identificador estable del escenario. |
| `descripcion` | Texto | Nombre descriptivo de la condición del escenario. |
| `deposito_id` | Texto, referencia a `nodos.nodo_id` | Depósito de salida y regreso; `N00` en los tres casos. |
| `capacidad_cajas` | Entero positivo, cajas | Máxima carga total al iniciar el recorrido. |
| `limite_tiempo_min` | Entero positivo, minutos | Máxima suma de viaje y servicio de todo el recorrido, incluido el regreso. |

| Escenario | Capacidad | Límite total | Cambio respecto de la base |
|---|---:|---:|---|
| `E_BASE` | 18 cajas | 130 minutos | Condición de referencia. |
| `E_CAPACIDAD` | 12 cajas | 130 minutos | Disminuye solo la capacidad. |
| `E_TIEMPO` | 18 cajas | 95 minutos | Disminuye solo el tiempo disponible. |

Cada escenario se resuelve como un caso independiente. Un pedido atendido en uno sigue disponible al estudiar los otros; no hay reparto de pedidos entre escenarios ni consumo acumulado de recursos entre ellos. Todos los pedidos son atendibles individualmente bajo las condiciones de `E_BASE`; eso no implica que puedan atenderse todos juntos.

## Reglas del recorrido y del servicio

El recorrido comienza y termina en el depósito del escenario. Puede repetir nodos y conexiones. Puede pasar por un centro sin atender su pedido, y puede usar centros e intersecciones como puntos de tránsito. **Pasar por un nodo no equivale a entregar un pedido:** solo los pedidos elegidos y efectivamente atendidos suman prioridad y tiempo de servicio.

No hay ventanas horarias, horas de apertura, precedencias entre pedidos, entregas parciales ni tiempos que dependan de la hora. El límite temporal se aplica al recorrido completo. Volver a pasar por el depósito durante un recorrido no permite recargar cajas ni reiniciar ese límite.

Un plan se describe con estos tres datos:

1. `escenario_id`: el escenario al que corresponde.
2. `pedidos_atendidos`: lista de `pedido_id` distintos que se entregan completos.
3. `recorrido`: lista ordenada de `nodo_id`, desde el depósito hasta el depósito, incluyendo **todos los nodos intermedios por los que se circula**. Cada par consecutivo debe ser una conexión publicada.

Todo centro asociado a un pedido de `pedidos_atendidos` debe aparecer en `recorrido`. Si un centro aparece varias veces, el pedido se atiende una sola vez; las demás apariciones son tránsito. Un centro que aparece en el recorrido pero cuyo pedido no figura en la lista es únicamente tránsito. No basta dar una lista de centros elegidos si entre ellos faltan las conexiones efectivamente recorridas.

La carga se obtiene sumando las cajas de los pedidos atendidos. El tiempo de viaje es la suma de `tiempo_min` de **cada paso** del recorrido. El tiempo de servicio es la suma de `servicio_min` de los pedidos atendidos. El tiempo total es viaje más servicio. El plan debe respetar tanto la capacidad como el límite temporal, permitiéndose la igualdad con cada límite.

## Objetivo y comparación de resultados

El objetivo principal es **maximizar la suma de prioridad de los pedidos completos atendidos**. Entre dos planes factibles con la misma suma de prioridad, se prefiere el que tenga **menor tiempo total, viaje más servicio**. Si también empatan en tiempo total, ambos tienen el mismo valor según estos criterios; no se impone otro desempate.

El número de pedidos o de cajas no sustituye la suma de prioridad. Atender más pedidos no es necesariamente mejor si su prioridad total es menor. La factibilidad se comprueba antes de comparar los objetivos.

## Reproducción de los CSV

Se necesita Python 3 y únicamente su biblioteca estándar. No hay semilla aleatoria: el archivo incluye los valores fijos de esta versión, en su orden de publicación. Desde la carpeta del paquete:

```sh
python3 generar_datos.py --salida ./datos_reproducidos
```

El comando crea la carpeta indicada y escribe los cuatro CSV con exactamente los mismos bytes que los publicados. Si se omite `--salida`, se escriben en la carpeta del generador. Los cuatro nombres de CSV se sobrescriben si ya existen en el destino. El generador no modifica este `LEEME.md` y no necesita acceso a Internet.

Conserven los datos adaptados en una carpeta identificada por separado, junto con el registro de cambios; no los confundan con este paquete de referencia. El generador reproduce únicamente los CSV originales, no las adaptaciones del grupo. La consigna del trabajo define los resultados y documentos que deben entregar.
