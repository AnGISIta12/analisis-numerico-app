"""Método de punto fijo usando scipy.optimize.fixed_point (iteración simple)."""
import warnings

import numpy as np
from scipy.optimize import fixed_point

from algoritmos.funciones import crear_funcion, derivar


def resolver_punto_fijo(texto_g: str, x0: float,
                        tol: float = 1e-6, max_iter: int = 100) -> dict:
    """Busca x tal que x = g(x), partiendo de x0.

    method="iteration" hace la iteración clásica x_{n+1} = g(x_n);
    sin eso SciPy usa aceleración de Steffensen.
    """
    g, expresion = crear_funcion(texto_g)
    dg, derivada = derivar(expresion)

    try:
        with warnings.catch_warnings(), np.errstate(all="ignore"):
            warnings.simplefilter("ignore")
            raiz = float(fixed_point(g, x0, xtol=tol, maxiter=max_iter,
                                     method="iteration"))
        convergio = True
    except (RuntimeError, OverflowError, FloatingPointError):
        raise ValueError(
            f"No convergió en {max_iter} iteraciones. "
            "Prueba otro despeje de g(x) u otro x0 (debe cumplirse |g'(x)| < 1 cerca de la raíz)"
        )

    return {
        "raiz": raiz,
        "g_raiz": float(g(raiz)),
        "dg_raiz": float(dg(raiz)),  # |g'| < 1 explica por qué convergió
        "convergio": convergio,
        "expresion": expresion,
        "derivada": derivada,
        "g": g,
    }
