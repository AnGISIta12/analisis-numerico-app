"""Pantalla de factorización LUP. El cálculo está en algoritmos/sistemas_lineales/lup.py."""
import streamlit as st

from algoritmos.sistemas_lineales.lup import resolver_lup
from interfaces.sistemas_lineales.componentes import (
    entrada_sistema, mostrar_matriz, mostrar_solucion, mostrar_vector)


def mostrar():
    st.header("Factorización LUP")
    st.caption("Como LU, pero con pivoteo parcial: PA = LU, donde P es la "
               "matriz de permutación que reordena las filas.")

    A, b = entrada_sistema("lup")

    if not st.button("Factorizar y resolver", type="primary"):
        return

    try:
        r = resolver_lup(A, b)
    except ValueError as e:
        st.error(str(e))
        return

    mostrar_solucion(r["x"], r["residuo"])

    st.subheader("Factores (PA = LU)")
    mostrar_matriz("P", r["P"])
    mostrar_matriz("L", r["L"])
    mostrar_matriz("U", r["U"])
    st.subheader("Lado derecho permutado")
    mostrar_vector("Pb", r["Pb"])
