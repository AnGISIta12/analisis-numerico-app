"""Piezas de interfaz que repiten las pantallas de sistemas lineales:
la tabla para escribir A y b, y cómo se muestran matrices y soluciones."""
import numpy as np
import pandas as pd
import streamlit as st

EJEMPLO_3X3 = ([[4, -1, 1], [4, -8, 1], [-2, 1, 5]], [7, -21, 15])  # solución (2, 4, 3)


def _ejemplo(n):
    if n == 3:
        return EJEMPLO_3X3
    # Diagonal dominante con solución (1, 1, ..., 1)
    A = np.ones((n, n)) + (n - 1) * np.eye(n)
    return A.tolist(), A.sum(axis=1).tolist()


def entrada_sistema(prefijo: str):
    """Pide n y muestra una tabla editable con [A | b]. Devuelve (A, b)."""
    n = st.number_input("Tamaño del sistema (n)", min_value=2, max_value=8,
                        value=3, step=1, key=f"{prefijo}_n")
    n = int(n)

    A, b = _ejemplo(n)
    columnas = [f"x{j + 1}" for j in range(n)]
    tabla = pd.DataFrame(A, columns=columnas, dtype=float)
    tabla["b"] = np.asarray(b, dtype=float)

    st.caption("Escribe los coeficientes de A y la columna b")
    editada = st.data_editor(tabla, key=f"{prefijo}_tabla_{n}",
                             hide_index=True, width="stretch")

    datos = editada.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    return datos[:, :n], datos[:, n]


def _num(v):
    v = 0.0 if abs(v) < 1e-12 else v
    return f"{v:.6g}"


def mostrar_matriz(nombre: str, M, aumentada: bool = False):
    """Muestra una matriz en LaTeX. Si aumentada, dibuja la barra antes de la última columna."""
    M = np.atleast_2d(M)
    filas, cols = M.shape
    formato = ("c" * (cols - 1) + "|c") if aumentada else "c" * cols
    cuerpo = r" \\ ".join(" & ".join(_num(v) for v in fila) for fila in M)
    st.latex(rf"{nombre} = \left[\begin{{array}}{{{formato}}} {cuerpo} \end{{array}}\right]")


def mostrar_vector(nombre: str, v):
    mostrar_matriz(nombre, np.asarray(v).reshape(-1, 1))


def mostrar_solucion(x, residuo: float):
    st.success("Solución: " + ", ".join(f"x{i + 1} = {_num(v)}" for i, v in enumerate(x)))
    st.caption(f"Residuo ‖Ax − b‖∞ = {residuo:.2e}")
