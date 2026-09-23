"""Pantalla de eliminación de Gauss. El cálculo está en algoritmos/sistemas_lineales/gauss.py."""
import streamlit as st

from algoritmos.sistemas_lineales.gauss import resolver_gauss
from interfaces.sistemas_lineales.componentes import (
    entrada_sistema, mostrar_matriz, mostrar_solucion)


def mostrar():
    st.header("Eliminación de Gauss")
    st.caption("Lleva la matriz aumentada [A | b] a forma triangular superior "
               "y despeja con sustitución hacia atrás.")

    A, b = entrada_sistema("gauss")

    if not st.button("Resolver", type="primary"):
        return

    try:
        r = resolver_gauss(A, b)
    except ValueError as e:
        st.error(str(e))
        return

    mostrar_solucion(r["x"], r["residuo"])

    st.subheader("Matriz escalonada")
    mostrar_matriz(r"[U \mid c]", r["escalonada"], aumentada=True)
    if r["intercambios"]:
        texto = ", ".join(f"F{i} ↔ F{j}" for i, j in r["intercambios"])
        st.info(f"Hubo pivotes cero; se intercambiaron filas: {texto}")
