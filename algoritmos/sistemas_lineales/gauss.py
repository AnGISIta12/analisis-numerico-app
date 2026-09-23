"""Eliminación de Gauss.

- La matriz aumentada escalonada se obtiene con sympy en aritmética exacta:
  la U de la descomposición LU de [A | b] es justamente el resultado de la
  eliminación hacia adelante (restar múltiplos de filas). Si aparece un pivote
  cero, sympy intercambia filas y se informa.
- La solución se calcula con numpy.linalg.solve.
"""
import numpy as np
import sympy as sp

from algoritmos.sistemas_lineales.validacion import validar_sistema


def resolver_gauss(A, b) -> dict:
    A, b = validar_sistema(A, b)

    aumentada = np.column_stack([A, b])
    exacta = sp.Matrix(*aumentada.shape,
                       lambda i, j: sp.Rational(str(aumentada[i, j])))
    _, escalonada, intercambios = exacta.LUdecomposition()

    x = np.linalg.solve(A, b)

    return {
        "x": x,
        "escalonada": np.array(escalonada.evalf(), dtype=float),
        "intercambios": [(i + 1, j + 1) for i, j in intercambios],
        "residuo": float(np.linalg.norm(A @ x - b, np.inf)),
    }
