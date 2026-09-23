"""Pantalla del método de la secante. El cálculo está en algoritmos/secante.py."""
import numpy as np
import pandas as pd
import streamlit as st
import sympy as sp

from algoritmos.raices.secante import resolver_secante


def mostrar():
    st.header("Método de la secante")
    st.caption("Como Newton, pero cambia la derivada por la pendiente entre "
               "los dos últimos puntos. No necesita que encierren la raíz.")

    texto = st.text_input("f(x)", value="x**3 - x - 2",
                          help="Usa x como variable. Ej: sin(x) - x/2, exp(x) - 3, x^2 - 4")

    col1, col2 = st.columns(2)
    x0 = col1.number_input("x₀", value=1.0, format="%.4f")
    x1 = col2.number_input("x₁", value=2.0, format="%.4f")

    col3, col4 = st.columns(2)
    tol = col3.number_input("Tolerancia", value=1e-6, min_value=1e-15, format="%.1e")
    max_iter = col4.number_input("Máx. iteraciones", value=50, min_value=1, step=1)

    if not st.button("Calcular raíz", type="primary"):
        return

    try:
        r = resolver_secante(texto, x0, x1, tol, int(max_iter))
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

    st.latex(f"f(x) = {sp.latex(r['expresion'])}")

    izq = min(x0, x1, r["raiz"]) - 0.5
    der = max(x0, x1, r["raiz"]) + 0.5
    xs = np.linspace(izq, der, 300)
    with np.errstate(all="ignore"):
        ys = np.broadcast_to(r["f"](xs), xs.shape).astype(float)
    st.line_chart(pd.DataFrame({"f(x)": ys, "y = 0": 0.0}, index=xs))
