"""Método de bisección usando scipy.optimize.bisect."""
from scipy.optimize import bisect

from algoritmos.funciones import crear_funcion


def resolver_biseccion(texto_funcion: str, a: float, b: float,
                       tol: float = 1e-6, max_iter: int = 100) -> dict:
    """Busca una raíz de f en [a, b].

    Devuelve un diccionario con la raíz, el número de iteraciones,
    si convergió, f(raíz), la expresión y la función (para graficarla).
    Lanza ValueError si los datos de entrada no son válidos.
    """
    if a >= b:
        raise ValueError("a debe ser menor que b")

    f, expresion = crear_funcion(texto_funcion)
    fa, fb = float(f(a)), float(f(b))

    if fa * fb > 0:
        raise ValueError(
            f"f(a) = {fa:.4g} y f(b) = {fb:.4g} tienen el mismo signo; "
            "prueba otro intervalo"
        )

    raiz, info = bisect(f, a, b, xtol=tol, maxiter=max_iter,
                        full_output=True, disp=False)

    return {
        "raiz": raiz,
        "f_raiz": float(f(raiz)),
        "iteraciones": info.iterations,
        "convergio": info.converged,
        "expresion": expresion,
        "f": f,
    }
