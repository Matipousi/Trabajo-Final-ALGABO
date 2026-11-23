"""
verificador.py — Control INDEPENDIENTE de factibilidad y valores de un plan.

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Finalidad: no confiar en lo que dice cada algoritmo sobre su propio plan.
Este módulo recibe el plan "en crudo" (lista de pedidos + secuencia de nodos)
y recalcula todo directamente desde conexiones.csv, SIN usar Dijkstra ni la
matriz de distancias. Si un algoritmo tuviera un error, acá aparece.

Reglas comprobadas (sección 2.1 de la consigna y LEEME.md):
  1. El recorrido empieza y termina en el depósito.
  2. Cada par de nodos consecutivos es una conexión existente y abierta.
  3. Los pedidos atendidos son distintos y pertenecen al escenario.
  4. El nodo de cada pedido atendido aparece en el recorrido.
  5. Cajas totales <= capacidad.
  6. Viaje + servicio <= límite de tiempo.
"""


def verificar_plan(datos, escenario, pedidos_atendidos, recorrido):
    errores = []

    # Tiempos de las conexiones abiertas, guardados en ambos sentidos.
    tiempo_tramo = {}
    for c in datos["conexiones"]:
        if c["id"] in escenario["cerradas"]:
            continue
        tiempo_tramo[(c["origen"], c["destino"])] = c["tiempo"]
        tiempo_tramo[(c["destino"], c["origen"])] = c["tiempo"]

    # Regla 1: inicio y fin en el depósito.
    dep = escenario["deposito"]
    if not recorrido or recorrido[0] != dep or recorrido[-1] != dep:
        errores.append("El recorrido no empieza y termina en el depósito")

    # Regla 2: cada paso usa una conexión existente; se suma su tiempo.
    viaje = 0
    for a, b in zip(recorrido, recorrido[1:]):
        if (a, b) not in tiempo_tramo:
            errores.append(f"No existe conexión abierta {a}-{b}")
        else:
            viaje += tiempo_tramo[(a, b)]

    # Regla 3: pedidos distintos y del escenario.
    if len(set(pedidos_atendidos)) != len(pedidos_atendidos):
        errores.append("Hay pedidos repetidos")
    for p in pedidos_atendidos:
        if p not in escenario["pedidos"]:
            errores.append(f"El pedido {p} no participa en este escenario")

    # Regla 4: cada pedido atendido tiene su centro en el recorrido.
    for p in pedidos_atendidos:
        if p in datos["pedidos"] and datos["pedidos"][p]["nodo"] not in recorrido:
            errores.append(f"El nodo del pedido {p} no está en el recorrido")

    # Totales (solo de los pedidos atendidos; pasar por un centro no suma).
    validos = [p for p in pedidos_atendidos if p in datos["pedidos"]]
    cajas = sum(datos["pedidos"][p]["cajas"] for p in validos)
    prioridad = sum(datos["pedidos"][p]["prioridad"] for p in validos)
    servicio = sum(datos["pedidos"][p]["servicio"] for p in validos)
    total = viaje + servicio

    # Reglas 5 y 6: capacidad y tiempo (la igualdad está permitida).
    if cajas > escenario["capacidad"]:
        errores.append(f"Cajas {cajas} > capacidad {escenario['capacidad']}")
    if total > escenario["limite"]:
        errores.append(f"Tiempo total {total} > límite {escenario['limite']}")

    return {
        "factible": not errores,
        "errores": errores,
        "prioridad": prioridad,
        "cajas": cajas,
        "viaje": viaje,
        "servicio": servicio,
        "total": total,
    }


def es_mejor(a, b):
    """Criterio de la consigna para comparar dos planes VERIFICADOS.
    Devuelve True si el plan a es estrictamente mejor que b.
    1) un plan no factible nunca le gana a uno factible;
    2) mayor prioridad; 3) ante empate, menor tiempo total."""
    if a["factible"] != b["factible"]:
        return a["factible"]
    if a["prioridad"] != b["prioridad"]:
        return a["prioridad"] > b["prioridad"]
    return a["total"] < b["total"]
