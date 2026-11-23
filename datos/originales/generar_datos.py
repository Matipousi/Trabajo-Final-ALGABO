#!/usr/bin/env python3
"""Reproduce los cuatro CSV del caso ficticio con Python 3, sin dependencias externas."""

import argparse
import csv
from pathlib import Path


NODOS = [
    ("N00", "deposito", "Deposito", "0.0", "0.0"),
    ("N01", "interseccion", "Cruce 01", "1.0", "0.0"),
    ("N02", "centro", "Centro 01", "2.0", "0.0"),
    ("N03", "centro", "Centro 02", "3.0", "0.0"),
    ("N04", "interseccion", "Cruce 02", "0.0", "1.0"),
    ("N05", "centro", "Centro 03", "1.0", "1.0"),
    ("N06", "centro", "Centro 04", "2.0", "1.0"),
    ("N07", "centro", "Centro 05", "3.0", "1.0"),
    ("N08", "interseccion", "Cruce 03", "0.0", "2.0"),
    ("N09", "centro", "Centro 06", "1.0", "2.0"),
    ("N10", "centro", "Centro 07", "2.0", "2.0"),
    ("N11", "centro", "Centro 08", "3.0", "2.0"),
    ("N12", "interseccion", "Cruce 04", "0.0", "3.0"),
    ("N13", "centro", "Centro 09", "1.0", "3.0"),
    ("N14", "interseccion", "Cruce 05", "2.0", "3.0"),
    ("N15", "centro", "Centro 10", "3.0", "3.0"),
]

CONEXIONES = [
    ("C01", "N00", "N01", 7),
    ("C02", "N01", "N02", 6),
    ("C03", "N02", "N03", 8),
    ("C04", "N04", "N05", 5),
    ("C05", "N05", "N06", 7),
    ("C06", "N06", "N07", 6),
    ("C07", "N08", "N09", 8),
    ("C08", "N09", "N10", 5),
    ("C09", "N10", "N11", 7),
    ("C10", "N12", "N13", 6),
    ("C11", "N13", "N14", 7),
    ("C12", "N14", "N15", 5),
    ("C13", "N00", "N04", 6),
    ("C14", "N01", "N05", 8),
    ("C15", "N02", "N06", 5),
    ("C16", "N03", "N07", 7),
    ("C17", "N04", "N08", 7),
    ("C18", "N05", "N09", 6),
    ("C19", "N06", "N10", 8),
    ("C20", "N07", "N11", 6),
    ("C21", "N08", "N12", 9),
    ("C22", "N09", "N13", 5),
    ("C23", "N10", "N14", 6),
    ("C24", "N11", "N15", 8),
    ("C25", "N00", "N05", 10),
    ("C26", "N01", "N06", 9),
    ("C27", "N05", "N10", 10),
    ("C28", "N06", "N11", 10),
    ("C29", "N09", "N14", 9),
]

PEDIDOS = [
    ("P01", "N02", 3, 11, 5),
    ("P02", "N03", 5, 19, 8),
    ("P03", "N05", 2, 8, 4),
    ("P04", "N06", 4, 15, 6),
    ("P05", "N07", 6, 24, 9),
    ("P06", "N09", 3, 13, 5),
    ("P07", "N10", 5, 20, 7),
    ("P08", "N11", 4, 18, 6),
    ("P09", "N13", 2, 10, 4),
    ("P10", "N15", 7, 30, 10),
]

ESCENARIOS = [
    ("E_BASE", "Condiciones de referencia", "N00", 18, 130),
    ("E_CAPACIDAD", "Menor capacidad de carga", "N00", 12, 130),
    ("E_TIEMPO", "Menor tiempo disponible", "N00", 18, 95),
]

ARCHIVOS = {
    "nodos.csv": (("nodo_id", "tipo", "nombre", "x", "y"), NODOS),
    "conexiones.csv": (("conexion_id", "origen", "destino", "tiempo_min"), CONEXIONES),
    "pedidos.csv": (("pedido_id", "nodo_id", "cajas", "prioridad", "servicio_min"), PEDIDOS),
    "escenarios.csv": (("escenario_id", "descripcion", "deposito_id", "capacidad_cajas", "limite_tiempo_min"), ESCENARIOS),
}


def escribir_csv(directorio):
    directorio.mkdir(parents=True, exist_ok=True)
    for nombre, (cabecera, filas) in ARCHIVOS.items():
        with (directorio / nombre).open("w", encoding="utf-8", newline="") as archivo:
            writer = csv.writer(archivo, delimiter=",", lineterminator="\n")
            writer.writerow(cabecera)
            writer.writerows(filas)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--salida", type=Path, default=Path(__file__).resolve().parent,
        help="Carpeta de destino; por defecto, la carpeta de este archivo.",
    )
    args = parser.parse_args()
    escribir_csv(args.salida)
    print("Se escribieron nodos.csv, conexiones.csv, pedidos.csv y escenarios.csv.")


if __name__ == "__main__":
    main()
