"""Pantalla del método de Newton-Raphson. El cálculo está en algoritmos/newton.py."""
import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from algoritmos.raices.newton import resolver_newton
from interfaces.notacion import texto_a_latex
from interfaces.raices.entrada_funcion import pedir_funcion


def mostrar():
    st.header("Método de Newton-Raphson")
    st.caption("Usa la recta tangente: x₍ₙ₊₁₎ = xₙ − f(xₙ) / f'(xₙ). "
               "La derivada se calcula automáticamente.")

    texto = pedir_funcion("f(x)", "x^3 - x - 2", clave="f_newton")

    x0 = st.number_input("x₀ (valor inicial)", value=1.5, format="%.4f")

    col1, col2 = st.columns(2)
    tol = col1.number_input("Tolerancia", value=1e-6, min_value=1e-15, format="%.1e")
    max_iter = col2.number_input("Máx. iteraciones", value=50, min_value=1, step=1)

    if not st.button("Calcular raíz", type="primary"):
        return

    try:
        r = resolver_newton(texto, x0, tol, int(max_iter))
    except ValueError as e:
        st.error(str(e))
        return

    if r["convergio"]:
        st.success(f"Raíz ≈ {r['raiz']:.10f}")
    else:
        st.warning(f"No convergió en {max_iter} iteraciones. Último valor: {r['raiz']:.10f}")

    m1, m2 = st.columns(2)
    m1.metric("Iteraciones", r["iteraciones"])
    m2.metric("f(raíz)", f"{r['f_raiz']:.2e}")

    st.latex(f"f(x) = {texto_a_latex(texto)[0]}")  # tal cual se escribió
    st.latex(f"f'(x) = {sp.latex(r['derivada'])}")

    ancho = max(1.0, abs(r["raiz"] - x0) * 1.5)
    xs = np.linspace(r["raiz"] - ancho, r["raiz"] + ancho, 300)
    with np.errstate(all="ignore"):
        ys = np.broadcast_to(r["f"](xs), xs.shape).astype(float)
    st.line_chart(pd.DataFrame({"f(x)": ys, "y = 0": 0.0}, index=xs))
