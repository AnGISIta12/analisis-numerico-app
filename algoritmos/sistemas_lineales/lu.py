"""Factorización LU (Doolittle, sin pivoteo) con sympy.

Matrix.LUdecomposition() devuelve L, U y la lista de intercambios de filas.
Si tuvo que intercambiar filas, la LU sin pivoteo no existe y se sugiere LUP.
"""
import numpy as np
import sympy as sp

from algoritmos.sistemas_lineales.validacion import validar_sistema


def resolver_lu(A, b) -> dict:
    A, b = validar_sistema(A, b)
    n = A.shape[0]

    A_exacta = sp.Matrix(n, n, lambda i, j: sp.Rational(str(A[i, j])))
    L, U, intercambios = A_exacta.LUdecomposition()

    if intercambios:
        raise ValueError("Aparece un pivote cero: A no tiene LU sin intercambiar filas. "
                         "Usa la factorización LUP")

    L = np.array(L.evalf(), dtype=float)
    U = np.array(U.evalf(), dtype=float)

    # Ly = b (sustitución hacia adelante) y Ux = y (sustitución hacia atrás)
    y = np.linalg.solve(L, b)
    x = np.linalg.solve(U, y)

    return {
        "L": L,
        "U": U,
        "y": y,
        "x": x,
        "residuo": float(np.linalg.norm(A @ x - b, np.inf)),
    }
