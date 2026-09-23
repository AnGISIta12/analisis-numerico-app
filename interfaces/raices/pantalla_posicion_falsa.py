"""Pantalla del método de posición falsa. El cálculo está en algoritmos/posicion_falsa.py."""
import numpy as np
import pandas as pd
import streamlit as st

from algoritmos.raices.posicion_falsa import resolver_posicion_falsa
from interfaces.notacion import texto_a_latex
from interfaces.raices.entrada_funcion import pedir_funcion


def mostrar():
    st.header("Método de posición falsa")
    st.caption("Como bisección, pero el nuevo punto es donde la recta entre "
               "(a, f(a)) y (b, f(b)) corta el eje x.")

    texto = pedir_funcion("f(x)", "x^3 - x - 2", clave="f_posicion_falsa")

    col1, col2 = st.columns(2)
    a = col1.number_input("a", value=1.0, format="%.4f")
    b = col2.number_input("b", value=2.0, format="%.4f")

    col3, col4 = st.columns(2)
    tol = col3.number_input("Tolerancia", value=1e-6, min_value=1e-15, format="%.1e")
    max_iter = col4.number_input("Máx. iteraciones", value=100, min_value=1, step=1)

    if not st.button("Calcular raíz", type="primary"):
        return

    try:
        r = resolver_posicion_falsa(texto, a, b, tol, int(max_iter))
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

    xs = np.linspace(a, b, 300)
    ys = np.broadcast_to(r["f"](xs), xs.shape)
    st.line_chart(pd.DataFrame({"f(x)": ys, "y = 0": 0.0}, index=xs))

    with st.expander("Ver iteraciones"):
        st.dataframe(pd.DataFrame(r["tabla"]), hide_index=True)
