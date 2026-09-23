"""Punto de entrada. Ejecutar con:  streamlit run main.py"""
import streamlit as st

from interfaces.barra_lateral import mostrar_barra_lateral
from interfaces.raices import (
    pantalla_biseccion,
    pantalla_newton,
    pantalla_posicion_falsa,
    pantalla_punto_fijo,
    pantalla_secante,
)
from interfaces.sistemas_lineales import (
    pantalla_gauss,
    pantalla_gauss_seidel,
    pantalla_lu,
    pantalla_lup,
)

st.set_page_config(page_title="Proyecto Numérico", layout="wide")

PANTALLAS = {
    "Raíces de ecuaciones": {
        "Bisección": pantalla_biseccion.mostrar,
        "Posición falsa": pantalla_posicion_falsa.mostrar,
        "Punto fijo": pantalla_punto_fijo.mostrar,
        "Newton-Raphson": pantalla_newton.mostrar,
        "Secante": pantalla_secante.mostrar,
    },
    "Sistemas lineales": {
        "Eliminación de Gauss": pantalla_gauss.mostrar,
        "Factorización LU": pantalla_lu.mostrar,
        "Factorización LUP": pantalla_lup.mostrar,
        "Gauss-Seidel": pantalla_gauss_seidel.mostrar,
    },
}

unidad, metodo = mostrar_barra_lateral()
PANTALLAS[unidad][metodo]()
