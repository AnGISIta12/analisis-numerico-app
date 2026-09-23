"""Convierte el texto que escribe el usuario en una función evaluable.

Se usa sympy en lugar de eval para no ejecutar código arbitrario.
Lo comparten todos los métodos numéricos.
"""
import sympy as sp

x = sp.Symbol("x")


def crear_funcion(texto: str):
    """Recibe algo como 'x**3 - x - 2' y devuelve (f, expresion).

    f es una función de Python que recibe floats o arrays de numpy.
    Lanza ValueError si el texto no es una función válida de x.
    """
    try:
        expresion = sp.sympify(texto.replace("^", "**"))
    except (sp.SympifyError, SyntaxError, TypeError):
        raise ValueError(f"No se pudo interpretar la función: '{texto}'")

    if not isinstance(expresion, sp.Expr):
        raise ValueError(f"No se pudo interpretar la función: '{texto}'")

    if expresion.free_symbols - {x}:
        raise ValueError("La función solo puede depender de x")

    f = sp.lambdify(x, expresion, "numpy")
    return f, expresion


def derivar(expresion):
    """Deriva simbólicamente la expresión. Devuelve (f', expresion_derivada)."""
    derivada = sp.diff(expresion, x)
    return sp.lambdify(x, derivada, "numpy"), derivada
