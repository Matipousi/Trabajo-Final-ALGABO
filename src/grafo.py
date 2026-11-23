"""
grafo.py — Representación de la red y caminos mínimos (Dijkstra).

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Finalidad: las dos estrategias (referencia y propuesta) deciden QUÉ pedidos
atender y en QUÉ ORDEN. Para eso necesitan saber cuánto se tarda, como mínimo,
en ir de un nodo "importante" (depósito o centro con pedido) a otro.
Eso lo calcula Dijkstra (tema 2 del curso), una vez por nodo importante.

Después, para entregar un plan verificable, cada tramo "centro A -> centro B"
se expande al camino real nodo por nodo (incluidos cruces y centros de paso).
"""

import heapq


def construir_adyacencia(nodos, conexiones, cerradas=frozenset()):
    """Lista de adyacencia de un grafo NO dirigido.

    adyacencia['N00'] = [('N01', 7), ('N04', 6), ...]
    Cada fila de conexiones.csv se agrega en los dos sentidos con el mismo
    tiempo. Las conexiones cuyo id esté en `cerradas` se omiten (escenarios
    de cierre de tramo)."""
    adyacencia = {nid: [] for nid in nodos}
    for c in conexiones:
        if c["id"] in cerradas:
            continue
        adyacencia[c["origen"]].append((c["destino"], c["tiempo"]))
        adyacencia[c["destino"]].append((c["origen"], c["tiempo"]))
    return adyacencia


def dijkstra(adyacencia, origen):
    """Dijkstra con heapq y patrón de entradas obsoletas (lazy), como en el curso.

    Devuelve:
      g:      {nodo: tiempo mínimo desde origen}
      previo: {nodo: nodo anterior en el camino mínimo}  (para reconstruir)
    Desempate: el heap ordena por (g, id_nodo), así que ante igual g se
    extrae primero el id menor. Esto hace el resultado reproducible."""
    g = {origen: 0}
    previo = {origen: None}
    frontera = [(0, origen)]
    extraidos = set()
    while frontera:
        g_actual, u = heapq.heappop(frontera)
        if u in extraidos:          # entrada obsoleta: ya se extrajo con menor g
            continue
        extraidos.add(u)
        for v, w in adyacencia[u]:
            nuevo = g_actual + w
            if v not in g or nuevo < g[v]:   # solo mejora estricta
                g[v] = nuevo
                previo[v] = u
                heapq.heappush(frontera, (nuevo, v))
    return g, previo


def reconstruir_camino(previo, destino):
    """Sigue los punteros 'previo' desde el destino hasta el origen y lo invierte."""
    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = previo[nodo]
    return camino[::-1]


def construir_instancia(datos, escenario):
    """Prepara todo lo que necesitan los algoritmos para UN escenario.

    Devuelve un diccionario con:
      deposito, capacidad, limite
      pedidos:  lista de ids de pedidos participantes (ordenada)
      nodo, cajas, prioridad, servicio: {pedido_id: valor}
      dist[a][b]:   tiempo mínimo entre nodos importantes a y b
      camino[a][b]: lista de nodos del camino mínimo de a a b
    """
    adyacencia = construir_adyacencia(datos["nodos"], datos["conexiones"],
                                      escenario["cerradas"])
    pedidos_ids = sorted(escenario["pedidos"])
    importantes = [escenario["deposito"]] + [datos["pedidos"][p]["nodo"] for p in pedidos_ids]

    dist, camino = {}, {}
    for a in importantes:
        g, previo = dijkstra(adyacencia, a)
        dist[a], camino[a] = {}, {}
        for b in importantes:
            if b not in g:
                raise ValueError(f"{b} no es alcanzable desde {a} en {escenario['id']}")
            dist[a][b] = g[b]
            camino[a][b] = reconstruir_camino(previo, b)

    info = datos["pedidos"]
    return {
        "escenario": escenario["id"],
        "deposito": escenario["deposito"],
        "capacidad": escenario["capacidad"],
        "limite": escenario["limite"],
        "pedidos": pedidos_ids,
        "nodo": {p: info[p]["nodo"] for p in pedidos_ids},
        "cajas": {p: info[p]["cajas"] for p in pedidos_ids},
        "prioridad": {p: info[p]["prioridad"] for p in pedidos_ids},
        "servicio": {p: info[p]["servicio"] for p in pedidos_ids},
        "dist": dist,
        "camino": camino,
    }


def expandir_recorrido(inst, orden_pedidos):
    """Convierte un orden de pedidos [P05, P02] en la secuencia completa de
    nodos: depósito -> ... -> nodo de P05 -> ... -> nodo de P02 -> ... -> depósito,
    usando los caminos mínimos. Así el plan incluye nodos de paso y regreso."""
    paradas = [inst["deposito"]] + [inst["nodo"][p] for p in orden_pedidos] + [inst["deposito"]]
    recorrido = [paradas[0]]
    for a, b in zip(paradas, paradas[1:]):
        recorrido += inst["camino"][a][b][1:]   # [1:] para no repetir el nodo a
    return recorrido


def tiempo_viaje_orden(inst, orden_pedidos):
    """Minutos de viaje de un orden de pedidos, usando la matriz dist."""
    paradas = [inst["deposito"]] + [inst["nodo"][p] for p in orden_pedidos] + [inst["deposito"]]
    return sum(inst["dist"][a][b] for a, b in zip(paradas, paradas[1:]))
