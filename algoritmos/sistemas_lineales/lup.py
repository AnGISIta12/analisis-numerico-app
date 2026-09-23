"""Factorización LUP (con pivoteo parcial) usando scipy.linalg.

scipy.linalg.lu devuelve P, L, U con A = P·L·U. En clase se escribe PA = LU,
así que la P "del libro" es la transpuesta de la de SciPy.
"""
import numpy as np
from scipy.linalg import lu, lu_factor, lu_solve

from algoritmos.sistemas_lineales.validacion import validar_sistema


def resolver_lup(A, b) -> dict:
    A, b = validar_sistema(A, b)

    P_scipy, L, U = lu(A)
    P = P_scipy.T  # ahora P·A = L·U

    x = lu_solve(lu_factor(A), b)

    return {
        "P": P,
        "L": L,
        "U": U,
        "Pb": P @ b,
        "x": x,
        "residuo": float(np.linalg.norm(A @ x - b, np.inf)),
    }
