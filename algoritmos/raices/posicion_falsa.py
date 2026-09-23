"""Método de posición falsa (regla falsa).

SciPy no lo incluye, así que está programado a mano. Guarda cada iteración
para poder mostrarlas en una tabla.
"""
from algoritmos.funciones import crear_funcion


def resolver_posicion_falsa(texto_funcion: str, a: float, b: float,
                            tol: float = 1e-6, max_iter: int = 100) -> dict:
    if a >= b:
        raise ValueError("a debe ser menor que b")

    f, expresion = crear_funcion(texto_funcion)
    fa, fb = float(f(a)), float(f(b))

    if fa * fb > 0:
        raise ValueError(
            f"f(a) = {fa:.4g} y f(b) = {fb:.4g} tienen el mismo signo; "
            "prueba otro intervalo"
        )

    tabla = []
    c_anterior = None
    convergio = False

    for i in range(1, max_iter + 1):
        # Corte con el eje x de la recta que une (a, f(a)) y (b, f(b))
        c = b - fb * (b - a) / (fb - fa)
        fc = float(f(c))
        tabla.append({"iteración": i, "a": a, "b": b, "c": c, "f(c)": fc})

        if fc == 0 or (c_anterior is not None and abs(c - c_anterior) < tol):
            convergio = True
            break

        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        c_anterior = c

    return {
        "raiz": c,
        "f_raiz": fc,
        "iteraciones": len(tabla),
        "convergio": convergio,
        "expresion": expresion,
        "f": f,
        "tabla": tabla,
    }
