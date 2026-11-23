"""
preparar_datos.py — Genera el dataset ADAPTADO a partir del original.

[Generado por IA: Claude Opus 5.5 (Claude Code), 23/11/2026. Ver DECLARACION_IA.md]

Finalidad: que la adaptación sea reproducible y quede documentada en código.
Lee datos/originales/, NO lo modifica, y escribe datos/adaptados/.

Pregunta que motiva la adaptación:
  "¿Cuándo conviene el método exacto (DP) y cuándo alcanza con el greedy?
   ¿Cambia la respuesta si (a) se cierra un tramo de salida del depósito
   con el tiempo ajustado, o (b) la red crece con un barrio nuevo lejano?"

Cambios (todos SINTÉTICOS, inventados para el estudio, igual que el original):
  1. Barrio nuevo: 6 centros N16–N21 (al este y al norte de la red original),
     11 conexiones nuevas C30–C40 con tiempos de 5 a 8 min (mismo rango que
     el original, 5–10) y 6 pedidos nuevos P11–P16, uno por centro.
  2. escenarios.csv gana dos columnas:
       pedidos_incluidos:   rango de pedidos que participan (P01-P10 o P01-P16)
       conexiones_cerradas: ids separados por ';' o 'ninguna'
  3. Escenarios nuevos:
       E_CIERRE        = E_TIEMPO + conexión C25 (N00–N05) cerrada
       E_AMPLIADO      = 16 pedidos, capacidad 24, límite 160
       E_AMPLIADO_BASE = 16 pedidos con los límites de E_BASE (18 cajas, 130 min)
  Los tres escenarios originales se conservan sin cambios (con P01-P10) para
  poder comparar contra ellos cambiando una sola condición a la vez.
"""

import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGEN = RAIZ / "datos" / "originales"
DESTINO = RAIZ / "datos" / "adaptados"

NODOS_NUEVOS = [  # nodo_id, tipo, nombre, x, y
    ("N16", "centro", "Centro 11", "4.0", "0.0"),
    ("N17", "centro", "Centro 12", "4.0", "1.0"),
    ("N18", "centro", "Centro 13", "4.0", "2.0"),
    ("N19", "centro", "Centro 14", "4.0", "3.0"),
    ("N20", "centro", "Centro 15", "1.0", "4.0"),
    ("N21", "centro", "Centro 16", "2.0", "4.0"),
]

CONEXIONES_NUEVAS = [  # conexion_id, origen, destino, tiempo_min
    ("C30", "N03", "N16", 6),
    ("C31", "N07", "N17", 5),
    ("C32", "N16", "N17", 7),
    ("C33", "N11", "N18", 6),
    ("C34", "N17", "N18", 6),
    ("C35", "N18", "N19", 5),
    ("C36", "N15", "N19", 7),
    ("C37", "N13", "N20", 6),
    ("C38", "N14", "N21", 5),
    ("C39", "N20", "N21", 6),
    ("C40", "N12", "N20", 8),
]

PEDIDOS_NUEVOS = [  # pedido_id, nodo_id, cajas, prioridad, servicio_min
    ("P11", "N16", 3, 12, 5),
    ("P12", "N17", 4, 16, 6),
    ("P13", "N18", 2, 9, 4),
    ("P14", "N19", 5, 22, 8),
    ("P15", "N20", 3, 14, 5),
    ("P16", "N21", 6, 25, 9),
]

ESCENARIOS = [  # id, descripción, depósito, capacidad, límite, pedidos, cerradas
    ("E_BASE", "Condiciones de referencia", "N00", 18, 130, "P01-P10", "ninguna"),
    ("E_CAPACIDAD", "Menor capacidad de carga", "N00", 12, 130, "P01-P10", "ninguna"),
    ("E_TIEMPO", "Menor tiempo disponible", "N00", 18, 95, "P01-P10", "ninguna"),
    ("E_CIERRE", "E_TIEMPO con la salida directa N00-N05 cerrada", "N00", 18, 95, "P01-P10", "C25"),
    ("E_AMPLIADO", "Red con barrio nuevo y mas recursos", "N00", 24, 160, "P01-P16", "ninguna"),
    ("E_AMPLIADO_BASE", "Red con barrio nuevo y limites de E_BASE", "N00", 18, 130, "P01-P16", "ninguna"),
]


def copiar_y_agregar(nombre, filas_nuevas):
    """Copia el CSV original y le agrega filas al final."""
    with open(ORIGEN / nombre, newline="", encoding="utf-8") as f:
        filas = list(csv.reader(f))
    filas += [list(map(str, fila)) for fila in filas_nuevas]
    with open(DESTINO / nombre, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(filas)


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)
    copiar_y_agregar("nodos.csv", NODOS_NUEVOS)
    copiar_y_agregar("conexiones.csv", CONEXIONES_NUEVAS)
    copiar_y_agregar("pedidos.csv", PEDIDOS_NUEVOS)
    with open(DESTINO / "escenarios.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["escenario_id", "descripcion", "deposito_id", "capacidad_cajas",
                    "limite_tiempo_min", "pedidos_incluidos", "conexiones_cerradas"])
        w.writerows(ESCENARIOS)
    print(f"Dataset adaptado escrito en {DESTINO}")


if __name__ == "__main__":
    main()
