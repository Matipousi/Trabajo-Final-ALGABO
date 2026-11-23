"""
experimentos.py — Programa principal: corre la comparación completa.

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Ejecutar desde la carpeta del proyecto:   python3 src/experimentos.py
Escribe todo en resultados/.

Etapas:
  1. Cargar y validar el dataset adaptado.
  2. Para cada escenario: resolver con referencia y propuesta, medir el
     tiempo de ejecución, verificar cada plan con el verificador independiente.
  3. Análisis de cierres: cerrar cada conexión de a una (E_TIEMPO) y ver
     cuánto cambia el resultado de cada método.
  4. Escalabilidad: instancias aleatorias de 8 a 24 pedidos (3 semillas por
     tamaño) para ver cuándo la DP deja de ser práctica.
  5. Guardar tablas (CSV), planes (JSON) y figuras (SVG).

Medición del tiempo de ejecución: time.perf_counter(), en milisegundos.
Se mide construir_instancia (incluye Dijkstra) + el método, porque ambos
métodos necesitan las distancias. Se repite 5 veces y se informa la mediana
(y el mínimo y máximo), para reducir el ruido del sistema operativo.
OJO: este tiempo (del programa) es una magnitud distinta de los minutos del plan.
"""

import csv
import json
import platform
import random
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from datos import cargar_datos, validar_datos
from grafo import construir_instancia
from verificador import verificar_plan, es_mejor
from referencia_greedy import resolver_greedy
from propuesta_dp import resolver_dp
import figuras

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "resultados"
REPETICIONES = 5
METODOS = {"referencia": resolver_greedy, "propuesta": resolver_dp}


def medir(resolver, datos, escenario, repeticiones=REPETICIONES):
    """Corre el método varias veces; devuelve el plan y los tiempos en ms."""
    tiempos = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        inst = construir_instancia(datos, escenario)
        plan = resolver(inst)
        tiempos.append((time.perf_counter() - t0) * 1000)
    return plan, tiempos


# ---------------------------------------------------------------- 2 ---------
def comparar_escenarios(datos):
    filas, planes_json = [], {}
    for esc in datos["escenarios"]:
        planes, verifs = {}, {}
        for clave, resolver in METODOS.items():
            plan, tiempos = medir(resolver, datos, esc)
            v = verificar_plan(datos, esc, plan["pedidos"], plan["recorrido"])
            planes[clave], verifs[clave] = plan, v
            filas.append({
                "escenario": esc["id"],
                "metodo": clave,
                "factible": "sí" if v["factible"] else "NO: " + "; ".join(v["errores"]),
                "pedidos_atendidos": " ".join(plan["orden"]),
                "n_atendidos": len(plan["pedidos"]),
                "prioridad": v["prioridad"],
                "cajas": v["cajas"],
                "capacidad": esc["capacidad"],
                "viaje_min": v["viaje"],
                "servicio_min": v["servicio"],
                "total_min": v["total"],
                "limite_min": esc["limite"],
                "ejec_ms_mediana": round(statistics.median(tiempos), 3),
                "ejec_ms_min": round(min(tiempos), 3),
                "ejec_ms_max": round(max(tiempos), 3),
                "estados_dp": plan.get("estados_generados", ""),
                "recorrido": "-".join(plan["recorrido"]),
            })
            planes_json[f"{esc['id']}|{clave}"] = {
                "escenario_id": esc["id"], "metodo": plan["metodo"],
                "pedidos_atendidos": plan["pedidos"], "orden_de_descarga": plan["orden"],
                "recorrido": plan["recorrido"], "verificacion": v,
            }
        # Quién gana según el criterio de la consigna (prioridad, luego tiempo).
        if es_mejor(verifs["propuesta"], verifs["referencia"]):
            ganador = "propuesta"
        elif es_mejor(verifs["referencia"], verifs["propuesta"]):
            ganador = "referencia"
        else:
            ganador = "empate"
        filas[-1]["ganador"] = filas[-2]["ganador"] = ganador
        (SALIDA / f"red_{esc['id']}.svg").write_text(
            figuras.svg_red_comparada(datos, esc, planes, verifs), encoding="utf-8")
    return filas, planes_json


# ---------------------------------------------------------------- 3 ---------
def analisis_cierres(datos, id_escenario="E_TIEMPO"):
    """Cierra cada conexión de a una y resuelve de nuevo con ambos métodos."""
    base = next(e for e in datos["escenarios"] if e["id"] == id_escenario)
    filas = []
    for c in datos["conexiones"]:
        if not c["id"] < "C30":      # solo la red original (el escenario usa P01-P10)
            continue
        esc = dict(base, cerradas={c["id"]}, id=f"{id_escenario}-sin-{c['id']}")
        fila = {"conexion_cerrada": c["id"], "tramo": f"{c['origen']}-{c['destino']}"}
        for clave, resolver in METODOS.items():
            plan = resolver(construir_instancia(datos, esc))
            v = verificar_plan(datos, esc, plan["pedidos"], plan["recorrido"])
            assert v["factible"]
            fila[f"prioridad_{clave}"] = v["prioridad"]
            fila[f"total_{clave}"] = v["total"]
        filas.append(fila)
    return filas


# ---------------------------------------------------------------- 4 ---------
def instancia_aleatoria(n_pedidos, semilla, familia):
    """Grilla sintética de 5x5 nodos (depósito en una esquina) con tiempos
    5–10 min, como el dataset. Los pedidos se ubican en n nodos al azar.
    familia 'ajustado': 18 cajas y 130 min (como E_BASE).
    familia 'holgado':  30 cajas y 200 min (poda menos: peor caso para la DP)."""
    rng = random.Random(semilla * 1000 + n_pedidos)
    lado = 5
    nodos = {f"G{f}{c}": {"tipo": "centro", "x": c, "y": f} for f in range(lado) for c in range(lado)}
    nodos["G00"]["tipo"] = "deposito"
    conexiones = []
    for f in range(lado):
        for c in range(lado):
            if c + 1 < lado:
                conexiones.append({"id": f"H{f}{c}", "origen": f"G{f}{c}", "destino": f"G{f}{c + 1}", "tiempo": rng.randint(5, 10)})
            if f + 1 < lado:
                conexiones.append({"id": f"V{f}{c}", "origen": f"G{f}{c}", "destino": f"G{f + 1}{c}", "tiempo": rng.randint(5, 10)})
    lugares = rng.sample([k for k in nodos if k != "G00"], n_pedidos)
    pedidos = {f"P{i + 1:02d}": {"nodo": lugares[i], "cajas": rng.randint(2, 7),
                                 "prioridad": rng.randint(8, 30), "servicio": rng.randint(4, 10)}
               for i in range(n_pedidos)}
    cap, lim = (18, 130) if familia == "ajustado" else (30, 200)
    esc = {"id": f"R{n_pedidos}-{familia}-s{semilla}", "deposito": "G00", "capacidad": cap,
           "limite": lim, "pedidos": sorted(pedidos), "cerradas": set()}
    return {"nodos": nodos, "conexiones": conexiones, "pedidos": pedidos}, esc


def escalabilidad(tamanos=(8, 10, 12, 14, 16, 18, 20, 22, 24), semillas=(1, 2, 3), tope_ms=60_000):
    filas = []
    seguir_dp = {"ajustado": True, "holgado": True}
    for familia in ("ajustado", "holgado"):
        for n in tamanos:
            for s in semillas:
                datos, esc = instancia_aleatoria(n, s, familia)
                fila = {"familia": familia, "n_pedidos": n, "semilla": s}
                for clave, resolver in METODOS.items():
                    if clave == "propuesta" and not seguir_dp[familia]:
                        fila.update({f"prioridad_{clave}": "", f"ms_{clave}": "", "estados_dp": "no se corrió"})
                        continue
                    plan, tiempos = medir(resolver, datos, esc, repeticiones=1)
                    v = verificar_plan(datos, esc, plan["pedidos"], plan["recorrido"])
                    assert v["factible"], v["errores"]
                    fila[f"prioridad_{clave}"] = v["prioridad"]
                    fila[f"total_{clave}"] = v["total"]
                    fila[f"ms_{clave}"] = round(tiempos[0], 3)
                    if clave == "propuesta":
                        fila["estados_dp"] = plan["estados_generados"]
                if fila.get("prioridad_propuesta") not in ("", None):
                    fila["brecha_greedy_%"] = round(100 * (fila["prioridad_propuesta"] - fila["prioridad_referencia"])
                                                    / fila["prioridad_propuesta"], 1)
                filas.append(fila)
                print(f"  {familia:8s} n={n:2d} s={s}: DP {fila.get('ms_propuesta')} ms, greedy {fila['ms_referencia']} ms")
            # Si la DP ya tarda más que el tope, no se prueban tamaños mayores.
            ms_dp = [f["ms_propuesta"] for f in filas if f["familia"] == familia and f["n_pedidos"] == n and f["ms_propuesta"] != ""]
            if ms_dp and statistics.median(ms_dp) > tope_ms:
                seguir_dp[familia] = False
    return filas


def guardar_csv(ruta, filas):
    campos = []
    for f in filas:
        campos += [k for k in f if k not in campos]
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        w = csv.DictWriter(archivo, fieldnames=campos, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


def main():
    SALIDA.mkdir(exist_ok=True)
    print("1) Cargando y validando datos/adaptados ...")
    datos = cargar_datos(RAIZ / "datos" / "adaptados")
    problemas = validar_datos(datos)
    if problemas:
        sys.exit("Datos con problemas:\n" + "\n".join(problemas))
    print("   sin problemas:", len(datos["nodos"]), "nodos,", len(datos["conexiones"]),
          "conexiones,", len(datos["pedidos"]), "pedidos,", len(datos["escenarios"]), "escenarios")

    print("2) Comparando métodos por escenario ...")
    filas, planes = comparar_escenarios(datos)
    guardar_csv(SALIDA / "resultados.csv", filas)
    (SALIDA / "planes.json").write_text(json.dumps(planes, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"   {'escenario':16s} {'método':10s} fact pri cajas viaje serv total  ms(med)")
    for f in filas:
        print(f"   {f['escenario']:16s} {f['metodo']:10s} {f['factible'][:3]:4s} {f['prioridad']:3d} {f['cajas']:5d} "
              f"{f['viaje_min']:5d} {f['servicio_min']:4d} {f['total_min']:5d}  {f['ejec_ms_mediana']:8.3f}")

    print("3) Análisis de cierres (E_TIEMPO, una conexión por vez) ...")
    cierres = analisis_cierres(datos)
    guardar_csv(SALIDA / "cierres.csv", cierres)

    print("4) Escalabilidad (instancias aleatorias, semillas 1, 2, 3) ...")
    esc_filas = escalabilidad()
    guardar_csv(SALIDA / "escalabilidad.csv", esc_filas)
    resumen = []
    for familia in ("ajustado", "holgado"):
        for n in sorted({f["n_pedidos"] for f in esc_filas}):
            grupo = [f for f in esc_filas if f["familia"] == familia and f["n_pedidos"] == n]
            for clave in METODOS:
                ms = [f[f"ms_{clave}"] for f in grupo if f.get(f"ms_{clave}") not in ("", None)]
                if ms:
                    resumen.append({"familia": familia, "n": n, "metodo": clave, "ms": statistics.median(ms)})
    (SALIDA / "escalabilidad.svg").write_text(figuras.svg_escalabilidad(resumen), encoding="utf-8")

    entorno = (f"Python {platform.python_version()} ({platform.python_implementation()})\n"
               f"Sistema: {platform.platform()}\nProcesador: {platform.machine()} {platform.processor()}\n"
               f"Medición: time.perf_counter, ms; {REPETICIONES} repeticiones por escenario (mediana); "
               f"1 por instancia aleatoria. Incluye construir_instancia (Dijkstra) + método.\n")
    (SALIDA / "entorno.txt").write_text(entorno, encoding="utf-8")
    print("Listo. Resultados en", SALIDA)


if __name__ == "__main__":
    main()
