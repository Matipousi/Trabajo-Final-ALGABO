"""
pruebas.py — Verificación: caso chico a mano, fuerza bruta y planes inválidos.

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Ejecutar:  python3 src/pruebas.py
Si todo está bien, imprime "OK" en cada prueba. Si algo falla, se detiene con
un AssertionError que dice qué prueba falló.

Tres tipos de controles (sección 4.3 de la consigna):
  A. Caso chico comprobable a mano (el de la guía del taller: N00–N05–N09).
  B. Fuerza bruta independiente: en los escenarios de 10 pedidos se prueban
     TODAS las secuencias de pedidos posibles y se confirma que la DP encuentra
     el mismo valor óptimo, y que el greedy nunca lo supera.
  C. Planes deliberadamente inválidos: el verificador debe rechazarlos.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from datos import cargar_datos, validar_datos
from grafo import construir_instancia, tiempo_viaje_orden
from verificador import verificar_plan
from referencia_greedy import resolver_greedy
from propuesta_dp import resolver_dp

RAIZ = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------- A ---------
def caso_chico(limite):
    """Red de la guía del taller: N00 --10-- N05 --6-- N09, capacidad 5.
    P03 en N05: 2 cajas, prioridad 8, 4 min.  P06 en N09: 3 cajas, prioridad 13, 5 min."""
    datos = {
        "nodos": {"N00": {"tipo": "deposito"}, "N05": {"tipo": "centro"}, "N09": {"tipo": "centro"}},
        "conexiones": [{"id": "A", "origen": "N00", "destino": "N05", "tiempo": 10},
                       {"id": "B", "origen": "N05", "destino": "N09", "tiempo": 6}],
        "pedidos": {"P03": {"nodo": "N05", "cajas": 2, "prioridad": 8, "servicio": 4},
                    "P06": {"nodo": "N09", "cajas": 3, "prioridad": 13, "servicio": 5}},
    }
    esc = {"id": f"CHICO_{limite}", "deposito": "N00", "capacidad": 5, "limite": limite,
           "pedidos": ["P03", "P06"], "cerradas": set()}
    return datos, esc


def prueba_caso_chico():
    # Cuentas a mano (tabla de la guía):
    #   Solo P03:  viaje 10+10 = 20, servicio 4,  total 24, prioridad 8
    #   Solo P06:  viaje 16+16 = 32, servicio 5,  total 37, prioridad 13
    #   P03 y P06: viaje 16+16 = 32, servicio 9,  total 41, prioridad 21
    # Con límite 40 -> solo P06 (13). Con límite 41 -> ambos (21), justo en el límite.
    esperado = {40: (["P06"], 13, 32, 5, 37), 41: (["P03", "P06"], 21, 32, 9, 41)}
    for limite, (pedidos, prio, viaje, serv, total) in esperado.items():
        datos, esc = caso_chico(limite)
        inst = construir_instancia(datos, esc)
        for resolver in (resolver_dp, resolver_greedy):
            plan = resolver(inst)
            v = verificar_plan(datos, esc, plan["pedidos"], plan["recorrido"])
            assert v["factible"], (resolver.__name__, limite, v["errores"])
            obtenido = (plan["pedidos"], v["prioridad"], v["viaje"], v["servicio"], v["total"])
            assert obtenido == (pedidos, prio, viaje, serv, total), (resolver.__name__, limite, obtenido)
        # El plan de ida y vuelta con ambos pasa DOS veces por N05 y descarga una sola vez.
        print(f"OK  caso chico, límite {limite}: {pedidos}, prioridad {prio}, total {total} — recorrido {'-'.join(plan['recorrido'])}")


# ---------------------------------------------------------------- B ---------
def fuerza_bruta(inst):
    """Prueba recursivamente todas las secuencias de pedidos distintos que
    respetan capacidad y tiempo. Es otro método exacto, escrito aparte de la DP,
    para contrastar. Solo es viable con pocos pedidos."""
    mejor = (0, 0)   # (prioridad, -total): plan vacío
    ids = inst["pedidos"]

    def explorar(orden, cajas, prio, serv):
        nonlocal mejor
        total = tiempo_viaje_orden(inst, orden) + serv
        if total > inst["limite"]:
            return   # ni este ni sus extensiones (que tardan más) son factibles
        mejor = max(mejor, (prio, -total))
        for p in ids:
            if p not in orden and cajas + inst["cajas"][p] <= inst["capacidad"]:
                explorar(orden + [p], cajas + inst["cajas"][p],
                         prio + inst["prioridad"][p], serv + inst["servicio"][p])

    explorar([], 0, 0, 0)
    return mejor[0], -mejor[1]


def prueba_fuerza_bruta():
    datos = cargar_datos(RAIZ / "datos" / "adaptados")
    for esc in datos["escenarios"]:
        if len(esc["pedidos"]) > 10:
            continue  # con 16 pedidos la fuerza bruta tarda demasiado
        inst = construir_instancia(datos, esc)
        fb = fuerza_bruta(inst)
        v_dp = verificar_plan(datos, esc, *(lambda p: (p["pedidos"], p["recorrido"]))(resolver_dp(inst)))
        v_gr = verificar_plan(datos, esc, *(lambda p: (p["pedidos"], p["recorrido"]))(resolver_greedy(inst)))
        assert (v_dp["prioridad"], v_dp["total"]) == fb, (esc["id"], fb, v_dp)
        assert v_gr["prioridad"] <= fb[0]
        print(f"OK  fuerza bruta {esc['id']}: óptimo (prioridad, total) = {fb}; DP coincide; greedy = {v_gr['prioridad']}")


# ---------------------------------------------------------------- C ---------
def prueba_planes_invalidos():
    datos = cargar_datos(RAIZ / "datos" / "adaptados")
    base = next(e for e in datos["escenarios"] if e["id"] == "E_BASE")
    cierre = next(e for e in datos["escenarios"] if e["id"] == "E_CIERRE")

    casos = [
        ("pasa capacidad (P01+P02+P05+P10 = 21 cajas > 18)", base,
         ["P01", "P02", "P05", "P10"], None),
        ("salto sin conexión N00->N09", base, ["P06"], ["N00", "N09", "N05", "N00"]),
        ("no regresa al depósito", base, ["P03"], ["N00", "N05"]),
        ("pedido cuyo centro no se visita", base, ["P06"], ["N00", "N05", "N00"]),
        ("usa la conexión cerrada C25 en E_CIERRE", cierre, ["P03"], ["N00", "N05", "N00"]),
        ("pasa el límite de tiempo", next(e for e in datos["escenarios"] if e["id"] == "E_TIEMPO"),
         ["P02", "P08", "P10"], None),
    ]
    for nombre, esc, pedidos, recorrido in casos:
        if recorrido is None:   # construir un recorrido válido con caminos mínimos
            inst = construir_instancia(datos, esc)
            from grafo import expandir_recorrido
            recorrido = expandir_recorrido(inst, pedidos)
        v = verificar_plan(datos, esc, pedidos, recorrido)
        assert not v["factible"], nombre
        if "tiempo" in nombre:   # que falle por la razón correcta
            assert any("Tiempo" in e for e in v["errores"]), v["errores"]
        print(f"OK  rechazado: {nombre} -> {v['errores'][0]}")


if __name__ == "__main__":
    assert validar_datos(cargar_datos(RAIZ / "datos" / "originales")) == []
    assert validar_datos(cargar_datos(RAIZ / "datos" / "adaptados")) == []
    print("OK  validación de datos originales y adaptados sin problemas")
    prueba_caso_chico()
    prueba_fuerza_bruta()
    prueba_planes_invalidos()
    print("\nTodas las pruebas pasaron.")
