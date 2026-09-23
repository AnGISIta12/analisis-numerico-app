"""Piezas de interfaz que repiten las pantallas de sistemas lineales:
la tabla para escribir A y b, y cómo se muestran matrices y soluciones."""
import numpy as np
import pandas as pd
import streamlit as st

from algoritmos.funciones import interpretar_numero
from interfaces import teclado
from interfaces.notacion import texto_a_latex

COLOR_SELECCION = "#2563eb"  # azul de la celda que edita el teclado

EJEMPLO_3X3 =([[4, -1, 1], [4, -8, 1], [-2, 1, 5]], [7, -21, 15])  # solución (2, 4, 3)


def _ejemplo(n):
    if n == 3:
        return EJEMPLO_3X3
    # Diagonal dominante con solución (1, 1, ..., 1)
    A = np.ones((n, n)) + (n - 1) * np.eye(n)
    return A.tolist(), A.sum(axis=1).tolist()


def _claves(prefijo: str, n: int) -> dict:
    return {
        "celdas": f"{prefijo}_celdas_{n}",    # textos de [A | b]
        "sel": f"{prefijo}_sel_{n}",          # celda seleccionada (i, j)
        "editor": f"{prefijo}_editor_{n}",    # texto que edita el teclado
        "version": f"{prefijo}_version_{n}",  # recrea la tabla a mano al cambiar
    }


def _seleccionar(prefijo: str, n: int, i: int, j: int):
    k = _claves(prefijo, n)
    st.session_state[k["sel"]] = (i, j)
    teclado.fijar_texto(k["editor"], st.session_state[k["celdas"]][i][j])


def _editar_a_mano(prefijo: str, n: int, clave_tabla: str):
    """Pasa lo escrito en la tabla a mano a las celdas del teclado."""
    k = _claves(prefijo, n)
    celdas = st.session_state[k["celdas"]]
    columnas = [f"x{j + 1}" for j in range(n)] + ["b"]
    for i, cambios in st.session_state[clave_tabla]["edited_rows"].items():
        for columna, valor in cambios.items():
            celdas[int(i)][columnas.index(columna)] = "" if valor is None else str(valor)
    i, j = st.session_state[k["sel"]]
    teclado.fijar_texto(k["editor"], celdas[i][j])
    st.session_state[k["version"]] += 1


def entrada_sistema(prefijo: str):
    """Pide n, muestra el sistema en notación matemática y las celdas de
    [A | b]. Se toca una celda y se escribe con el teclado matemático; las
    celdas aceptan expresiones como 1/3, √2, 2π o 2,5.

    Devuelve (A, b); las celdas vacías o inválidas quedan como NaN y
    validar_sistema las reporta al resolver.
    """
    n = st.number_input("Tamaño del sistema (n)", min_value=2, max_value=8,
                        value=3, step=1, key=f"{prefijo}_n")
    n = int(n)
    k = _claves(prefijo, n)
    columnas = [f"x{j + 1}" for j in range(n)] + ["b"]

    if k["celdas"] not in st.session_state:
        A, b = _ejemplo(n)
        st.session_state[k["celdas"]] = [[_num(v) for v in fila] + [_num(b[i])]
                                         for i, fila in enumerate(A)]
        st.session_state[k["sel"]] = (0, 0)
        st.session_state[k["version"]] = 0
        teclado.preparar(k["editor"], st.session_state[k["celdas"]][0][0])
    celdas = st.session_state[k["celdas"]]
    sel = st.session_state[k["sel"]]

    # Lo que escribió el teclado pasa a la celda seleccionada
    editor, cursor = teclado.estado(k["editor"])
    if celdas[sel[0]][sel[1]] != editor:
        celdas[sel[0]][sel[1]] = editor
        st.session_state[k["version"]] += 1

    valores = np.full((n, n + 1), np.nan)
    textos = [[None] * (n + 1) for _ in range(n)]  # None = celda inválida
    errores = []
    for i in range(n):
        for j in range(n + 1):
            try:
                valores[i, j], _ = interpretar_numero(celdas[i][j])
                textos[i][j] = celdas[i][j].strip()
            except ValueError as e:
                errores.append(f"fila {i + 1}, {columnas[j]}: {e}")

    st.latex(_latex_sistema(textos, valores))
    if errores:
        st.caption("⚠️ Revisa " + "; ".join(errores))

    st.caption("Toca una celda y escríbela con el teclado "
               "(acepta 1/3, √2, 2π, 2,5 ...)")
    # Una columna angosta vacía separa A de b, como la barra de [A | b]
    anchos = [1] * n + [0.25, 1]
    posicion = list(range(n)) + [n + 1]
    # La celda seleccionada va en azul para no confundirla con el rojo de "Resolver"
    st.markdown(f"""<style>
    .st-key-{prefijo}_celda_{n}_{sel[0]}_{sel[1]} button {{
        background-color: {COLOR_SELECCION}; border-color: {COLOR_SELECCION}; color: #ffffff;
    }}
    .st-key-{prefijo}_celda_{n}_{sel[0]}_{sel[1]} button:hover {{
        filter: brightness(1.15); color: #ffffff;
    }}
    </style>""", unsafe_allow_html=True)
    encabezado = st.columns(anchos)
    for j in range(n + 1):
        encabezado[posicion[j]].caption(f"$x_{{{j + 1}}}$" if j < n else "$b$")
    for i in range(n):
        fila = st.columns(anchos)
        for j in range(n + 1):
            elegida = (i, j) == sel
            latex = texto_a_latex(celdas[i][j], cursor if elegida else None,
                                  decimal_coma=True)[0]
            fila[posicion[j]].button(
                f"${latex}$", key=f"{prefijo}_celda_{n}_{i}_{j}", width="stretch",
                on_click=_seleccionar, args=(prefijo, n, i, j))

    teclado.dibujar_teclado(k["editor"], deshabilitadas={"x"})

    with st.expander("✏️ Escribir a mano"):
        clave_tabla = f"{prefijo}_tabla_{n}_{st.session_state[k['version']]}"
        st.data_editor(
            pd.DataFrame(celdas, columns=columnas), key=clave_tabla,
            hide_index=True, width="stretch",
            column_config={c: st.column_config.TextColumn(c) for c in columnas},
            on_change=_editar_a_mano, args=(prefijo, n, clave_tabla),
        )

    return valores[:, :n], valores[:, n]


def _suma_afuera(texto: str) -> bool:
    """True si hay un + o − fuera de paréntesis (sin contar el signo inicial)."""
    nivel = 0
    for i, ch in enumerate(texto):
        if ch == "(":
            nivel += 1
        elif ch == ")":
            nivel -= 1
        elif ch in "+-−" and nivel == 0 and texto[:i].strip():
            return True
    return False


def _latex_coeficiente(texto: str):
    """Separa el signo del coeficiente tal cual está escrito.

    Devuelve (signo, latex): '-1/3' → ('-', '\\frac{1}{3}'); '1-√2' → ('+', '(1 - √2)').
    """
    if _suma_afuera(texto):
        signo, magnitud = "+", texto
    elif texto[:1] in "-−":
        signo, magnitud = "-", texto[1:].strip()
    else:
        signo, magnitud = "+", texto.lstrip("+").strip()
    latex = texto_a_latex(magnitud, decimal_coma=True)[0]
    if _suma_afuera(magnitud):
        latex = rf"\left({latex}\right)"
    return signo, latex


def _latex_sistema(textos, valores) -> str:
    """El sistema como ecuaciones alineadas: 4x₁ − x₂ + x₃ = 7.

    Cada coeficiente se ve tal cual se escribió (4/2 no se vuelve 2).
    Los coeficientes cero se omiten y las celdas inválidas se ven como □.
    """
    n = len(textos)
    filas = []
    for i in range(n):
        celdas = []
        hay_termino = False
        for j in range(n):
            texto, valor = textos[i][j], valores[i, j]
            variable = f"x_{{{j + 1}}}"
            if texto is None:
                signo, termino = "+", rf"\square\, {variable}"
            elif valor == 0:
                signo, termino = "", ""
            else:
                signo, coef = _latex_coeficiente(texto)
                if coef == "1":
                    coef = ""
                termino = f"{coef} {variable}"

            if termino and not hay_termino:
                # El primer término no lleva '+' y el '−' va pegado
                termino = ("-" if signo == "-" else "") + termino
                signo = ""
                hay_termino = True
            if j == 0:
                celdas.append(termino)
            else:
                celdas += [signo, termino]

        if not hay_termino:
            celdas[0] = "0"

        texto = textos[i][n]
        derecho = r"\square" if texto is None else texto_a_latex(texto, decimal_coma=True)[0]
        filas.append(" & ".join(celdas + ["=", derecho]))

    formato = "r" + "cr" * (n - 1) + "cl"
    cuerpo = r" \\ ".join(filas)
    return rf"\left\{{ \begin{{array}}{{{formato}}} {cuerpo} \end{{array}} \right."


def _num(v):
    v = 0.0 if abs(v) < 1e-12 else v
    return f"{v:.6g}"


def mostrar_matriz(nombre: str, M, aumentada: bool = False):
    """Muestra una matriz en LaTeX. Si aumentada, dibuja la barra antes de la última columna."""
    M = np.atleast_2d(M)
    filas, cols = M.shape
    formato = ("c" * (cols - 1) + "|c") if aumentada else "c" * cols
    cuerpo = r" \\ ".join(" & ".join(_num(v) for v in fila) for fila in M)
    st.latex(rf"{nombre} = \left[\begin{{array}}{{{formato}}} {cuerpo} \end{{array}}\right]")


def mostrar_vector(nombre: str, v):
    mostrar_matriz(nombre, np.asarray(v).reshape(-1, 1))


def mostrar_solucion(x, residuo: float):
    st.success("Solución: " + ", ".join(f"x{i + 1} = {_num(v)}" for i, v in enumerate(x)))
    st.caption(f"Residuo ‖Ax − b‖∞ = {residuo:.2e}")
