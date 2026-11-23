"""
propuesta_dp.py — PROPUESTA: programación dinámica exacta (Held–Karp) con poda.

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Idea: es el mismo Held–Karp de la ADI 1 (tema 4), adaptado a este problema.
En la ADI 1 había que visitar TODOS los monumentos; acá se puede elegir un
subconjunto. Por eso, en vez de mirar solo la tabla final, se mira cada
subconjunto posible de pedidos y se elige el de mayor prioridad que entre.

Tabla (en lenguaje llano):
  estados[S][j] = (minutos mínimos de VIAJE para salir del depósito, atender
                   exactamente los pedidos del conjunto S y estar parado en j,
                   el último pedido atendido;  quién fue el anterior a j)
  El conjunto S se guarda como un número binario ("máscara"): el bit i vale 1
  si el pedido i está en el conjunto. Ej. con 3 pedidos, 101 = {pedido 0, pedido 2}.

Paso: desde (S, j) se puede ir a un pedido k que no esté en S:
  estados[S + k][k] = estados[S][j] + dist(j, k)   (si mejora)

PODA (idea de ramificación y poda, tema 5): un estado se descarta si
  - las cajas de S + k superan la capacidad, o
  - viaje hasta k + servicio de S + k + volver directo al depósito > límite.
  "Volver directo" es una cota optimista válida: cualquier extensión del
  recorrido tarda al menos eso (dist son caminos mínimos). Así nunca se
  descarta un plan que podría ser factible.

Al final, para cada conjunto S alcanzado:
  viaje(S)  = min_j estados[S][j] + dist(j, depósito)
  total(S)  = viaje(S) + servicio(S)
y se elige el S factible de mayor prioridad; ante empate, menor total.

Garantía: el plan es ÓPTIMO para el escenario. Razón: cualquier recorrido
válido (aunque repita nodos) entre dos pedidos consecutivos tarda al menos el
camino mínimo de Dijkstra, y la DP revisa todos los órdenes de todos los
subconjuntos que no fueron podados (y la poda solo quita imposibles).
Limitación: la cantidad de estados crece como 2^n * n; con muchos pedidos
(y límites holgados que poden poco) se vuelve lenta o se queda sin memoria.
"""

from grafo import expandir_recorrido


def resolver_dp(inst):
    ids = inst["pedidos"]
    n = len(ids)
    dep = inst["deposito"]
    nodo = [inst["nodo"][p] for p in ids]
    cajas = [inst["cajas"][p] for p in ids]
    serv = [inst["servicio"][p] for p in ids]
    prio = [inst["prioridad"][p] for p in ids]
    D = inst["dist"]
    cap, lim = inst["capacidad"], inst["limite"]

    # Distancias con índices: d[i][k] entre pedidos, ida[k] desde depósito,
    # vuelta[k] hacia depósito (red no dirigida: son iguales, se separan por claridad).
    d = [[D[nodo[i]][nodo[k]] for k in range(n)] for i in range(n)]
    ida = [D[dep][nodo[k]] for k in range(n)]
    vuelta = [D[nodo[k]][dep] for k in range(n)]

    # Cajas, servicio y prioridad acumulados de cada máscara (se calculan al vuelo).
    cajas_de = {0: 0}
    serv_de = {0: 0}

    # estados[mascara][j] = (viaje, j_anterior); j = -1 significa "en el depósito".
    estados = {0: {-1: (0, None)}}
    capa = [0]                       # máscaras con k pedidos; se avanza capa a capa
    estados_generados = 1

    while capa:
        siguiente = set()
        for S in capa:
            for j, (viaje_j, _) in estados[S].items():
                for k in range(n):
                    bit = 1 << k
                    if S & bit:
                        continue                         # k ya está en S
                    nuevas_cajas = cajas_de[S] + cajas[k]
                    if nuevas_cajas > cap:
                        continue                         # poda por capacidad
                    viaje_k = viaje_j + (ida[k] if j == -1 else d[j][k])
                    nuevo_serv = serv_de[S] + serv[k]
                    if viaje_k + nuevo_serv + vuelta[k] > lim:
                        continue                         # poda por tiempo (cota optimista)
                    T = S | bit
                    if T not in estados:
                        estados[T] = {}
                        cajas_de[T] = nuevas_cajas
                        serv_de[T] = nuevo_serv
                        siguiente.add(T)
                    actual = estados[T].get(k)
                    # Guardar si mejora; desempate: anterior con índice menor.
                    if actual is None or (viaje_k, j) < (actual[0], actual[1]):
                        if actual is None:
                            estados_generados += 1
                        estados[T][k] = (viaje_k, j)
        capa = sorted(siguiente)

    # Elegir el mejor subconjunto factible.
    mejor = None   # (clave de comparación, S, j_final, viaje)
    for S, por_ultimo in estados.items():
        if S == 0:
            viaje, j_fin = 0, -1
        else:
            viaje, j_fin = min((v + vuelta[j], j) for j, (v, _) in por_ultimo.items())
        total = viaje + serv_de[S]
        if total > lim:
            continue
        p_total = sum(prio[i] for i in range(n) if S >> i & 1)
        elegidos = tuple(ids[i] for i in range(n) if S >> i & 1)
        # Mayor prioridad, luego menor total, luego lista de ids menor (reproducible).
        clave = (-p_total, total, elegidos)
        if mejor is None or clave < mejor[0]:
            mejor = (clave, S, j_fin, viaje)

    # Reconstruir el orden siguiendo los punteros "anterior" hacia atrás.
    _, S, j, _ = mejor
    orden_idx = []
    while j != -1:
        orden_idx.append(j)
        _, previo = estados[S][j]
        S ^= 1 << j
        j = previo
    orden = [ids[i] for i in reversed(orden_idx)]

    return {
        "metodo": "Propuesta: DP Held–Karp con poda",
        "pedidos": sorted(orden),
        "orden": orden,
        "recorrido": expandir_recorrido(inst, orden),
        "estados_generados": estados_generados,
    }
