"""Método de Newton-Raphson usando scipy.optimize.newton.

La derivada se calcula con sympy, así el usuario solo escribe f(x).
"""
import warnings

from scipy.optimize import newton

from algoritmos.funciones import crear_funcion, derivar


def resolver_newton(texto_funcion: str, x0: float,
                    tol: float = 1e-6, max_iter: int = 100) -> dict:
    f, expresion = crear_funcion(texto_funcion)
    df, derivada = derivar(expresion)

    if float(df(x0)) == 0:
        raise ValueError("f'(x0) = 0: la tangente es horizontal, prueba otro x0")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        raiz, info = newton(f, x0, fprime=df, tol=tol, maxiter=max_iter,
                            full_output=True, disp=False)

    return {
        "raiz": float(raiz),
        "f_raiz": float(f(raiz)),
        "iteraciones": info.iterations,
        "convergio": info.converged,
        "expresion": expresion,
        "derivada": derivada,
        "f": f,
    }
