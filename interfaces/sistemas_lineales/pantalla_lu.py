"""Pantalla de factorización LU. El cálculo está en algoritmos/sistemas_lineales/lu.py."""
import streamlit as st

from algoritmos.sistemas_lineales.lu import resolver_lu
from interfaces.sistemas_lineales.componentes import (
    entrada_sistema, mostrar_matriz, mostrar_solucion, mostrar_vector)


def mostrar():
    st.header("Factorización LU")
    st.caption("Escribe A = LU (L triangular inferior con unos en la diagonal, "
               "U triangular superior). Luego resuelve Ly = b y Ux = y.")

    A, b = entrada_sistema("lu")

    if not st.button("Factorizar y resolver", type="primary"):
        return

    try:
        r = resolver_lu(A, b)
    except ValueError as e:
        st.error(str(e))
        return

    mostrar_solucion(r["x"], r["residuo"])

    st.subheader("Factores")
    mostrar_matriz("L", r["L"])
    mostrar_matriz("U", r["U"])
    st.subheader("Sustitución hacia adelante (Ly = b)")
    mostrar_vector("y", r["y"])
