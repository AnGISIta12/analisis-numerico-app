"""Validaciones comunes para los métodos de sistemas lineales."""
import numpy as np


def validar_sistema(A, b):
    """Convierte A y b a arrays de numpy y revisa que el sistema tenga solución única.

    Lanza ValueError con un mensaje claro si algo falla.
    """
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float).ravel()

    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A debe ser una matriz cuadrada")
    if b.shape[0] != A.shape[0]:
        raise ValueError("b debe tener tantas filas como A")
    if not (np.all(np.isfinite(A)) and np.all(np.isfinite(b))):
        raise ValueError("Hay celdas vacías o valores no numéricos")
    if np.linalg.matrix_rank(A) < A.shape[0]:
        raise ValueError("A es singular (det = 0): el sistema no tiene solución única")

    return A, b
