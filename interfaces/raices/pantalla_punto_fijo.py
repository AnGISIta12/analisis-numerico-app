"""Pantalla del método de punto fijo. El cálculo está en algoritmos/punto_fijo.py."""
import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from algoritmos.raices.punto_fijo import resolver_punto_fijo


def mostrar():
    st.header("Método de punto fijo")
    st.caption("Reescribe f(x) = 0 como x = g(x) e itera x₍ₙ₊₁₎ = g(xₙ). "
               "Converge si |g'(x)| < 1 cerca de la raíz.")

    texto = st.text_input("g(x)", value="(x + 2)**(1/3)",
                          help="Escribe el despeje x = g(x). Ej: para x³ − x − 2 = 0, "
                               "g(x) = (x + 2)**(1/3)")

    x0 = st.number_input("x₀ (valor inicial)", value=1.0, format="%.4f")

    col1, col2 = st.columns(2)
    tol = col1.number_input("Tolerancia", value=1e-6, min_value=1e-15, format="%.1e")
    max_iter = col2.number_input("Máx. iteraciones", value=100, min_value=1, step=1)

    if not st.button("Calcular punto fijo", type="primary"):
        return

    try:
        r = resolver_punto_fijo(texto, x0, tol, int(max_iter))
    except ValueError as e:
        st.error(str(e))
        return

    st.success(f"Punto fijo ≈ {r['raiz']:.10f}")

    m1, m2 = st.columns(2)
    m1.metric("g(x*) − x*", f"{r['g_raiz'] - r['raiz']:.2e}")
    m2.metric("|g'(x*)|", f"{abs(r['dg_raiz']):.4f}")

    st.latex(f"g(x) = {sp.latex(r['expresion'])}")
    st.latex(f"g'(x) = {sp.latex(r['derivada'])}")

    # g(x) contra y = x: el punto fijo es donde se cruzan
    ancho = max(1.0, abs(r["raiz"] - x0) * 1.5)
    xs = np.linspace(r["raiz"] - ancho, r["raiz"] + ancho, 300)
    with np.errstate(all="ignore"):
        ys = np.broadcast_to(r["g"](xs), xs.shape).astype(float)
    st.line_chart(pd.DataFrame({"g(x)": ys, "y = x": xs}, index=xs))
