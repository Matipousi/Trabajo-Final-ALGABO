"""
figuras.py — Dibujos en SVG (solo biblioteca estándar, sin matplotlib).

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Finalidad: mostrar en el informe (1) la red con el recorrido de cada método y
(2) cómo crece el tiempo de ejecución con la cantidad de pedidos.
Un SVG es texto: se puede abrir en el navegador o insertar en el informe HTML.
Las coordenadas x,y de nodos.csv solo se usan para dibujar (no para tiempos).
"""

import math

COLOR = {"propuesta": "#2a78d6", "referencia": "#eb6834"}   # azul / naranja
TINTA, TINTA_2, GRIS, FONDO = "#0b0b0b", "#52514e", "#c9c8c2", "#fcfcfb"


def _panel_red(datos, escenario, plan, verif, clave, x0, ancho, alto):
    """Dibuja un panel con la red y el recorrido de un plan."""
    nodos = datos["nodos"]
    xs = [n["x"] for n in nodos.values()]
    ys = [n["y"] for n in nodos.values()]
    margen = 45
    esc = min((ancho - 2 * margen) / max(1, max(xs) - min(xs)),
              (alto - 2 * margen - 50) / max(1, max(ys) - min(ys)))

    def px(nid):  # y crece hacia arriba en los datos, hacia abajo en SVG
        n = nodos[nid]
        return x0 + margen + (n["x"] - min(xs)) * esc, 60 + margen + (max(ys) - n["y"]) * esc

    color = COLOR[clave]
    partes = []
    titulo = "Propuesta: DP exacta" if clave == "propuesta" else "Referencia: greedy"
    partes.append(f'<text x="{x0 + 12}" y="22" font-size="14" font-weight="600" fill="{TINTA}">{titulo}</text>')
    partes.append(
        f'<text x="{x0 + 12}" y="40" font-size="11.5" fill="{TINTA_2}">prioridad {verif["prioridad"]} · '
        f'{verif["cajas"]}/{escenario["capacidad"]} cajas · {verif["total"]}/{escenario["limite"]} min '
        f'({verif["viaje"]} viaje + {verif["servicio"]} servicio)</text>')

    # Todas las conexiones (gris); las cerradas, punteadas en rojo.
    for c in datos["conexiones"]:
        (a, b), (c2, d) = px(c["origen"]), px(c["destino"])
        if c["id"] in escenario["cerradas"]:
            partes.append(f'<line x1="{a}" y1="{b}" x2="{c2}" y2="{d}" stroke="#e34948" stroke-width="2" stroke-dasharray="5 4"/>')
            partes.append(f'<text x="{(a + c2) / 2 + 4}" y="{(b + d) / 2 - 4}" font-size="10" fill="#b3261e">cerrada</text>')
        else:
            partes.append(f'<line x1="{a}" y1="{b}" x2="{c2}" y2="{d}" stroke="{GRIS}" stroke-width="1"/>')
            partes.append(f'<text x="{(a + c2) / 2 + 2}" y="{(b + d) / 2 - 2}" font-size="8.5" fill="#8a8984">{c["tiempo"]}</text>')

    # Recorrido del plan: cada paso como segmento de color (los repetidos se ven más gruesos).
    usos = {}
    for a, b in zip(plan["recorrido"], plan["recorrido"][1:]):
        k = frozenset((a, b))
        usos[k] = usos.get(k, 0) + 1
    for k, veces in usos.items():
        a, b = tuple(k)
        (x1, y1), (x2, y2) = px(a), px(b)
        partes.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                      f'stroke-width="{2 + 2 * (veces - 1)}" stroke-linecap="round" opacity="0.85"/>')

    # Nodos: depósito cuadrado, centros círculos (rellenos si se atienden), cruces chicos.
    atendidos = {datos["pedidos"][p]["nodo"]: p for p in plan["pedidos"]}
    orden_visita = {datos["pedidos"][p]["nodo"]: i + 1 for i, p in enumerate(plan["orden"])}
    pedido_de = {v["nodo"]: k for k, v in datos["pedidos"].items() if k in escenario["pedidos"]}
    for nid, n in nodos.items():
        x, y = px(nid)
        if n["tipo"] == "deposito":
            partes.append(f'<rect x="{x - 8}" y="{y - 8}" width="16" height="16" rx="3" fill="{TINTA}"/>')
            partes.append(f'<text x="{x - 10}" y="{y + 22}" font-size="10" fill="{TINTA}">{nid} depósito</text>')
        elif n["tipo"] == "centro":
            relleno = color if nid in atendidos else "#ffffff"
            partes.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{relleno}" stroke="{TINTA_2}" stroke-width="1.2"/>')
            if nid in orden_visita:
                partes.append(f'<text x="{x}" y="{y + 3.5}" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">{orden_visita[nid]}</text>')
            etiqueta = pedido_de.get(nid, "")
            partes.append(f'<text x="{x + 11}" y="{y + 14}" font-size="9" fill="{TINTA_2}">{nid} {etiqueta}</text>')
        else:
            partes.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{TINTA_2}"/>')
            partes.append(f'<text x="{x + 6}" y="{y + 12}" font-size="8.5" fill="#8a8984">{nid}</text>')
    return "".join(partes)


def svg_red_comparada(datos, escenario, planes, verifs):
    """Dos paneles (referencia | propuesta) para un escenario."""
    ancho, alto = 420, 400
    if max(n["y"] for n in datos["nodos"].values()) > 3:
        alto = 470
    cuerpo = (_panel_red(datos, escenario, planes["referencia"], verifs["referencia"], "referencia", 0, ancho, alto)
              + _panel_red(datos, escenario, planes["propuesta"], verifs["propuesta"], "propuesta", ancho, ancho, alto))
    nota = ("Números blancos = orden de descarga. Círculo vacío = centro no atendido (puede ser de paso). "
            "Trazo más grueso = tramo recorrido dos veces.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {2 * ancho} {alto + 20}" '
            f'font-family="Helvetica, Arial, sans-serif"><rect width="100%" height="100%" fill="{FONDO}"/>'
            f'{cuerpo}<text x="12" y="{alto + 10}" font-size="10" fill="{TINTA_2}">{nota}</text></svg>')


def svg_escalabilidad(filas):
    """Gráfico de líneas, eje Y logarítmico: mediana del tiempo de ejecución (ms)
    según la cantidad de pedidos. Color = método; trazo = familia de instancias."""
    ancho, alto = 760, 380
    izq, der, arr, aba = 70, 170, 40, 50
    ns = sorted({f["n"] for f in filas})
    ts = [f["ms"] for f in filas]
    lo, hi = math.floor(math.log10(min(ts))), math.ceil(math.log10(max(ts)))

    def X(n):
        return izq + (n - ns[0]) / (ns[-1] - ns[0]) * (ancho - izq - der)

    def Y(ms):
        return arr + (hi - math.log10(ms)) / (hi - lo) * (alto - arr - aba)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" font-family="Helvetica, Arial, sans-serif">',
         f'<rect width="100%" height="100%" fill="{FONDO}"/>',
         f'<text x="{izq}" y="22" font-size="13" font-weight="600" fill="{TINTA}">Tiempo de ejecución (mediana de 3 semillas, ms, escala log)</text>']
    for e in range(lo, hi + 1):
        y = Y(10 ** e)
        etiqueta = f"{10 ** e:g}"
        p.append(f'<line x1="{izq}" x2="{ancho - der}" y1="{y}" y2="{y}" stroke="#e6e5e0"/>')
        p.append(f'<text x="{izq - 8}" y="{y + 4}" font-size="10.5" fill="{TINTA_2}" text-anchor="end">{etiqueta}</text>')
    for n in ns:
        p.append(f'<text x="{X(n)}" y="{alto - aba + 18}" font-size="10.5" fill="{TINTA_2}" text-anchor="middle">{n}</text>')
    p.append(f'<text x="{(izq + ancho - der) / 2}" y="{alto - 12}" font-size="11" fill="{TINTA_2}" text-anchor="middle">cantidad de pedidos</text>')

    series = [("propuesta", "ajustado", "DP · ajustado", ""), ("propuesta", "holgado", "DP · holgado", "6 4"),
              ("referencia", "ajustado", "Greedy · ajustado", ""), ("referencia", "holgado", "Greedy · holgado", "6 4")]
    for i, (metodo, familia, nombre, guion) in enumerate(series):
        pts = sorted((f["n"], f["ms"]) for f in filas if f["metodo"] == metodo and f["familia"] == familia)
        if not pts:
            continue
        d = " ".join(f"{X(n):.1f},{Y(ms):.1f}" for n, ms in pts)
        p.append(f'<polyline points="{d}" fill="none" stroke="{COLOR[metodo]}" stroke-width="2" stroke-dasharray="{guion}"/>')
        for n, ms in pts:
            p.append(f'<circle cx="{X(n):.1f}" cy="{Y(ms):.1f}" r="4" fill="{COLOR[metodo]}" stroke="{FONDO}" stroke-width="2"/>')
        # Leyenda a la derecha (identidad nunca solo por color: también trazo y texto).
        ly = arr + 20 + i * 22
        p.append(f'<line x1="{ancho - der + 14}" x2="{ancho - der + 40}" y1="{ly}" y2="{ly}" stroke="{COLOR[metodo]}" stroke-width="2" stroke-dasharray="{guion}"/>')
        p.append(f'<text x="{ancho - der + 46}" y="{ly + 4}" font-size="11" fill="{TINTA}">{nombre}</text>')
    p.append("</svg>")
    return "".join(p)
