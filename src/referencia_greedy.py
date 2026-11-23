"""
referencia_greedy.py — SOLUCIÓN DE REFERENCIA: greedy de inserción.

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Idea (estrategia voraz / greedy, como Greedy Best-First del tema 3 pero sobre
planes): se arranca con un plan vacío (depósito -> depósito) y en cada paso se
agrega UN pedido, el que parece "más rentable" ahora mismo, sin volver atrás.

  rentabilidad = prioridad del pedido / minutos extra que agrega al plan

"Minutos extra" = desvío de viaje por meterlo en la mejor posición del orden
actual (inserción más barata) + su tiempo de servicio.

Solo se consideran pedidos que entran en la capacidad y en el límite de tiempo.
Se para cuando ningún pedido restante entra.

Garantía: siempre devuelve un plan FACTIBLE (cada inserción se comprueba).
Limitación: NO garantiza el óptimo; una decisión temprana no se deshace.
Costo: cerca de n^3 operaciones (n = pedidos): muy rápido aun con muchos pedidos.
"""

from grafo import expandir_recorrido, tiempo_viaje_orden


def resolver_greedy(inst):
    dist, dep = inst["dist"], inst["deposito"]
    orden = []            # orden de visita de los pedidos elegidos
    cajas_usadas = 0
    tiempo_usado = 0      # viaje + servicio del plan actual

    while True:
        mejor = None      # (rentabilidad, -extra, pedido, posición)
        for p in inst["pedidos"]:
            if p in orden:
                continue
            if cajas_usadas + inst["cajas"][p] > inst["capacidad"]:
                continue  # no entra en el vehículo
            # Paradas actuales: depósito, centros elegidos, depósito.
            paradas = [dep] + [inst["nodo"][q] for q in orden] + [dep]
            # Probar insertar p entre cada par de paradas consecutivas.
            for pos in range(len(paradas) - 1):
                a, b = paradas[pos], paradas[pos + 1]
                k = inst["nodo"][p]
                desvio = dist[a][k] + dist[k][b] - dist[a][b]
                extra = desvio + inst["servicio"][p]
                if tiempo_usado + extra > inst["limite"]:
                    continue  # se pasaría del límite de tiempo
                candidato = (inst["prioridad"][p] / extra, -extra, p, pos)
                # Desempate explícito: mayor rentabilidad; luego menor extra;
                # luego menor id de pedido (por eso se compara p "al revés").
                if (mejor is None or candidato[:2] > mejor[:2]
                        or (candidato[:2] == mejor[:2] and p < mejor[2])):
                    mejor = candidato
        if mejor is None:
            break         # ningún pedido restante entra: fin
        _, menos_extra, p, pos = mejor
        orden.insert(pos, p)
        cajas_usadas += inst["cajas"][p]
        tiempo_usado += -menos_extra

    # Comprobación interna de consistencia (el verificador independiente
    # vuelve a calcular todo desde las conexiones).
    assert tiempo_usado == tiempo_viaje_orden(inst, orden) + sum(inst["servicio"][q] for q in orden)

    return {
        "metodo": "Referencia: greedy de inserción",
        "pedidos": sorted(orden),
        "orden": orden,
        "recorrido": expandir_recorrido(inst, orden),
    }
