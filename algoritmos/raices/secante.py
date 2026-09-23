"""Método de la secante usando scipy.optimize.newton sin derivada.

Si a newton() no se le pasa fprime y se le da x1, usa la secante.
"""
import warnings

from scipy.optimize import newton

from algoritmos.funciones import crear_funcion


def resolver_secante(texto_funcion: str, x0: float, x1: float,
                     tol: float = 1e-6, max_iter: int = 100) -> dict:
    if x0 == x1:
        raise ValueError("x0 y x1 deben ser distintos")

    f, expresion = crear_funcion(texto_funcion)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        raiz, info = newton(f, x0, x1=x1, tol=tol, maxiter=max_iter,
                            full_output=True, disp=False)

    return {
        "raiz": float(raiz),
        "f_raiz": float(f(raiz)),
        "iteraciones": info.iterations,
        "convergio": info.converged,
        "expresion": expresion,
        "f": f,
    }
