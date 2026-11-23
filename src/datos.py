"""
datos.py — Carga y validación de los CSV del caso.

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Finalidad: leer los cuatro CSV (nodos, conexiones, pedidos, escenarios) y
convertirlos en estructuras simples de Python (diccionarios y listas).
Antes de resolver nada, se valida que los datos sean coherentes: si un dato
está mal, cualquier algoritmo daría un resultado sin sentido.

Solo se usa la biblioteca estándar (csv), para que el proyecto corra sin
instalar nada.
"""

import csv
from pathlib import Path

TIPOS_VALIDOS = {"deposito", "centro", "interseccion"}


def leer_csv(ruta):
    """Devuelve una lista de filas; cada fila es un diccionario {columna: texto}."""
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def expandir_rango_pedidos(texto):
    """Convierte 'P01-P10' en ['P01', ..., 'P10'].

    Se usa en escenarios.csv adaptado para indicar qué pedidos participan
    en cada escenario (el original usaba siempre los 10)."""
    inicio, fin = texto.split("-")
    a, b = int(inicio[1:]), int(fin[1:])
    return [f"P{i:02d}" for i in range(a, b + 1)]


def cargar_datos(carpeta):
    """Lee los cuatro CSV de `carpeta` y devuelve un diccionario con todo el caso.

    Estructura devuelta:
      nodos:      {'N00': {'tipo','nombre','x','y'}, ...}
      conexiones: [{'id','origen','destino','tiempo'}, ...]
      pedidos:    {'P01': {'nodo','cajas','prioridad','servicio'}, ...}
      escenarios: [{'id','descripcion','deposito','capacidad','limite',
                    'pedidos': [...], 'cerradas': set(...)}, ...]
    """
    carpeta = Path(carpeta)

    nodos = {}
    for f in leer_csv(carpeta / "nodos.csv"):
        if f["nodo_id"] in nodos:
            raise ValueError(f"nodo_id repetido: {f['nodo_id']}")
        nodos[f["nodo_id"]] = {
            "tipo": f["tipo"],
            "nombre": f["nombre"],
            "x": float(f["x"]),
            "y": float(f["y"]),
        }

    conexiones = []
    for f in leer_csv(carpeta / "conexiones.csv"):
        conexiones.append({
            "id": f["conexion_id"],
            "origen": f["origen"],
            "destino": f["destino"],
            "tiempo": int(f["tiempo_min"]),
        })

    pedidos = {}
    for f in leer_csv(carpeta / "pedidos.csv"):
        if f["pedido_id"] in pedidos:
            raise ValueError(f"pedido_id repetido: {f['pedido_id']}")
        pedidos[f["pedido_id"]] = {
            "nodo": f["nodo_id"],
            "cajas": int(f["cajas"]),
            "prioridad": int(f["prioridad"]),
            "servicio": int(f["servicio_min"]),
        }

    escenarios = []
    for f in leer_csv(carpeta / "escenarios.csv"):
        # Columnas agregadas en la adaptación. Si no están (dataset original),
        # se usan todos los pedidos y ninguna conexión cerrada.
        rango = f.get("pedidos_incluidos")
        lista_pedidos = expandir_rango_pedidos(rango) if rango else sorted(pedidos)
        texto_cerradas = f.get("conexiones_cerradas", "ninguna")
        cerradas = set() if texto_cerradas in ("", "ninguna") else set(texto_cerradas.split(";"))
        escenarios.append({
            "id": f["escenario_id"],
            "descripcion": f["descripcion"],
            "deposito": f["deposito_id"],
            "capacidad": int(f["capacidad_cajas"]),
            "limite": int(f["limite_tiempo_min"]),
            "pedidos": lista_pedidos,
            "cerradas": cerradas,
        })

    return {"nodos": nodos, "conexiones": conexiones,
            "pedidos": pedidos, "escenarios": escenarios}


def validar_datos(datos):
    """Revisa claves, valores y referencias. Devuelve una lista de problemas
    (vacía si todo está bien). No corrige nada: solo informa."""
    problemas = []
    nodos, conexiones = datos["nodos"], datos["conexiones"]
    pedidos, escenarios = datos["pedidos"], datos["escenarios"]

    # --- Nodos: tipos válidos y exactamente un depósito -----------------
    for nid, n in nodos.items():
        if n["tipo"] not in TIPOS_VALIDOS:
            problemas.append(f"Nodo {nid}: tipo desconocido '{n['tipo']}'")
    depositos = [nid for nid, n in nodos.items() if n["tipo"] == "deposito"]
    if len(depositos) != 1:
        problemas.append(f"Se esperaba 1 depósito y hay {len(depositos)}")

    # --- Conexiones: extremos existentes, tiempo positivo, sin repetidos --
    ids_vistos, pares_vistos = set(), set()
    for c in conexiones:
        if c["id"] in ids_vistos:
            problemas.append(f"conexion_id repetido: {c['id']}")
        ids_vistos.add(c["id"])
        for extremo in (c["origen"], c["destino"]):
            if extremo not in nodos:
                problemas.append(f"{c['id']}: el nodo {extremo} no existe")
        if c["origen"] == c["destino"]:
            problemas.append(f"{c['id']}: conecta un nodo consigo mismo")
        if c["tiempo"] <= 0:
            problemas.append(f"{c['id']}: tiempo no positivo ({c['tiempo']})")
        par = frozenset((c["origen"], c["destino"]))  # no dirigida: A-B = B-A
        if par in pares_vistos:
            problemas.append(f"{c['id']}: conexión duplicada entre {sorted(par)}")
        pares_vistos.add(par)

    # --- Pedidos: nodo válido, de tipo centro, un pedido por centro -------
    nodos_con_pedido = set()
    for pid, p in pedidos.items():
        if p["nodo"] not in nodos:
            problemas.append(f"Pedido {pid}: el nodo {p['nodo']} no existe")
        elif nodos[p["nodo"]]["tipo"] != "centro":
            problemas.append(f"Pedido {pid}: el nodo {p['nodo']} no es un centro")
        if p["nodo"] in nodos_con_pedido:
            problemas.append(f"Pedido {pid}: su centro ya tiene otro pedido")
        nodos_con_pedido.add(p["nodo"])
        for campo in ("cajas", "prioridad", "servicio"):
            if p[campo] <= 0:
                problemas.append(f"Pedido {pid}: {campo} no positivo")

    # --- Escenarios: depósito válido, límites positivos, referencias ------
    for e in escenarios:
        if e["deposito"] not in nodos or nodos[e["deposito"]]["tipo"] != "deposito":
            problemas.append(f"Escenario {e['id']}: depósito inválido")
        if e["capacidad"] <= 0 or e["limite"] <= 0:
            problemas.append(f"Escenario {e['id']}: capacidad o límite no positivo")
        for pid in e["pedidos"]:
            if pid not in pedidos:
                problemas.append(f"Escenario {e['id']}: pedido {pid} no existe")
        for cid in e["cerradas"]:
            if cid not in ids_vistos:
                problemas.append(f"Escenario {e['id']}: conexión cerrada {cid} no existe")
    return problemas
