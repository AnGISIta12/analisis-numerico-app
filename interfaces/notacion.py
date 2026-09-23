"""Convierte el texto de una función en LaTeX tal cual está escrito.

Solo sirve para mostrar: no simplifica ni reordena (sympy convertiría
'1/4 - 1/(9x)' en otra cosa), no falla con funciones a medio escribir
(lo que falta se ve como □) y puede dibujar el cursor del teclado.

Respeta la misma precedencia que usa algoritmos/funciones.py para calcular:
  + −  <  × ÷ y multiplicación implícita  <  − unario  <  ^
"""
import re

CURSOR = r"\textcolor{#f59e0b}{\vert}"
HUECO = r"\square"

FUNCIONES = {
    "sin": r"\sin", "cos": r"\cos", "tan": r"\tan",
    "sec": r"\sec", "csc": r"\csc", "cot": r"\cot",
    "asin": r"\sin^{-1}", "acos": r"\cos^{-1}", "atan": r"\tan^{-1}",
    "sinh": r"\sinh", "cosh": r"\cosh", "tanh": r"\tanh",
    "sen": r"\operatorname{sen}", "exp": r"\exp",
    "ln": r"\ln", "log": r"\log", "log10": r"\log_{10}",
}
RAICES = {"sqrt", "raiz"}

CONSTANTES = {"pi": r"\pi", "e": "e", "E": "e"}

# Caracteres del teclado que equivalen a un operador
OPERADORES = {"+": "+", "-": "-", "−": "-", "*": "*", "×": "*", "·": "*",
              "/": "/", "÷": "/", "^": "^"}

_TOKEN = re.compile(r"\s*(?:(\*\*)|(\d+\.?\d*|\.\d+)|([A-Za-z_]\w*)|(.))", re.ASCII)
# En las celdas de las tablas la coma es decimal (2,5); en f(x) separa argumentos
_TOKEN_COMA = re.compile(r"\s*(?:(\*\*)|(\d+[.,]?\d*|[.,]\d+)|([A-Za-z_]\w*)|(.))", re.ASCII)


class _Token:
    def __init__(self, tipo, texto, latex=None):
        self.tipo, self.texto = tipo, texto
        self.latex = latex if latex is not None else texto


def _tokenizar(texto: str, cursor, decimal_coma: bool):
    tokens = []
    pendiente = cursor is not None  # el cursor aún no se ha ubicado
    for m in (_TOKEN_COMA if decimal_coma else _TOKEN).finditer(texto):
        inicio, fin = m.start(m.lastindex), m.end()
        if pendiente and cursor <= inicio:
            tokens.append(_Token("CUR", ""))
            pendiente = False

        potencia, numero, nombre, otro = m.groups()
        if numero:
            latex = numero.replace(",", "{,}")  # sin {} LaTeX deja espacio tras la coma
            if pendiente and inicio < cursor < fin:  # cursor dentro del número
                corte = cursor - inicio
                latex = numero[:corte] + CURSOR + numero[corte:]
                pendiente = False
            tokens.append(_Token("NUM", numero, latex))
        elif nombre:
            tokens.append(_Token("NOMBRE", nombre))
        elif potencia:
            tokens.append(_Token("OP", "^"))
        elif otro in OPERADORES:
            tokens.append(_Token("OP", OPERADORES[otro]))
        elif otro == "π":
            tokens.append(_Token("NOMBRE", "pi"))
        elif otro == "√":
            tokens.append(_Token("NOMBRE", "sqrt"))
        elif otro in "²³":
            tokens.append(_Token("SUP", otro, "2" if otro == "²" else "3"))
        elif otro in "(),":
            tokens.append(_Token(otro, otro))
        else:
            seguro = otro if otro.isalnum() else "?"
            tokens.append(_Token("OTRO", otro, r"\text{" + seguro + "}"))

    if pendiente:
        tokens.append(_Token("CUR", ""))
    tokens.append(_Token("FIN", ""))
    return tokens


class _Traductor:
    def __init__(self, tokens):
        self.tokens, self.i, self.huecos = tokens, 0, 0

    # --- utilidades -------------------------------------------------------
    def actual(self):
        """Siguiente token real (ignora el cursor sin consumirlo)."""
        t = self.tokens[self.i]
        return self.tokens[self.i + 1] if t.tipo == "CUR" else t

    def cursor(self) -> str:
        """Consume el cursor si está justo aquí y devuelve su LaTeX."""
        if self.tokens[self.i].tipo == "CUR":
            self.i += 1
            return CURSOR
        return ""

    def avanzar(self):
        t = self.tokens[self.i]
        self.i += 1
        return t

    def hueco(self) -> tuple:
        self.huecos += 1
        return self.cursor() + HUECO, None

    def empieza_operando(self) -> bool:
        return self.actual().tipo in ("NUM", "NOMBRE", "(")

    # --- gramática --------------------------------------------------------
    # Cada regla devuelve (latex, interior): interior es el contenido sin
    # paréntesis cuando el nodo es un grupo, para quitarlos en fracciones
    # y exponentes como hace GeoGebra.

    def suma(self):
        izq, _ = self.producto()
        while self.actual().tipo == "OP" and self.actual().texto in "+-":
            c = self.cursor()
            op = self.avanzar().texto
            der, _ = self.producto()
            izq = f"{izq}{c} {op} {der}"
        return izq, None

    def producto(self):
        izq = self.unario()
        while True:
            t = self.actual()
            if t.tipo == "OP" and t.texto in "*/":
                c = self.cursor()
                op = self.avanzar().texto
                der = self.unario()
                if op == "*":
                    izq = (f"{izq[0]}{c} \\cdot {der[0]}", None)
                else:
                    izq = (rf"\frac{{{_sin_parentesis(izq)}{c}}}{{{_sin_parentesis(der)}}}", None)
            elif self.empieza_operando():  # multiplicación implícita: 2x
                # Entre dos números se pone '·' para que 2 3 no parezca 23
                separador = r" \cdot " if t.tipo == "NUM" else " "
                der = self.potencia()
                izq = (f"{izq[0]}{separador}{der[0]}", None)
            else:
                return izq

    def unario(self):
        t = self.actual()
        if t.tipo == "OP" and t.texto in "+-":
            c = self.cursor()
            op = self.avanzar().texto
            operando, _ = self.unario()
            return f"{c}{op}{operando}", None
        return self.potencia()

    def potencia(self):
        base = self.atomo()
        t = self.actual()
        if t.tipo == "OP" and t.texto == "^":
            c = self.cursor()
            self.avanzar()
            exponente = self.unario()  # a^b^c = a^(b^c)
            return f"{{{base[0]}{c}}}^{{{_sin_parentesis(exponente)}}}", None
        if t.tipo == "SUP":
            c = self.cursor()
            return f"{{{base[0]}{c}}}^{{{self.avanzar().latex}}}", None
        return base

    def atomo(self):
        c = self.cursor()
        t = self.actual()

        if t.tipo == "NUM":
            return c + self.avanzar().latex, None

        if t.tipo == "(":
            interior = self.grupo()
            return rf"{c}\left({interior}\right)", c + interior

        if t.tipo == "NOMBRE":
            nombre = self.avanzar().texto
            if nombre in FUNCIONES or nombre in RAICES or nombre == "abs":
                if self.actual().tipo == "(":
                    arg = self.grupo()
                elif self.empieza_operando():  # sin x
                    arg = self.potencia()[0]
                else:
                    arg = self.hueco()[0]
                if nombre in RAICES:
                    return rf"{c}\sqrt{{{arg}}}", None
                if nombre == "abs":
                    return rf"{c}\left|{arg}\right|", None
                return rf"{c}{FUNCIONES[nombre]}\left({arg}\right)", None
            if nombre in CONSTANTES:
                return c + CONSTANTES[nombre], None
            return c + nombre.replace("_", r"\_"), None

        # Falta un operando (ej. después de un '-' al final)
        if c:
            self.i -= 1  # devuelve el cursor para que quede antes del □
        return self.hueco()

    def grupo(self) -> str:
        """'(' expresión ')' → devuelve el interior. Si falta ')' se cierra solo."""
        self.cursor()  # un cursor antes de '(' ya lo puso quien llama
        self.avanzar()
        interior, _ = self.suma()
        while self.actual().tipo == ",":
            c = self.cursor()
            self.avanzar()
            siguiente, _ = self.suma()
            interior = f"{interior}{c}, {siguiente}"
        interior += self.cursor()
        if self.actual().tipo == ")":
            self.avanzar()
        return interior

    def todo(self) -> str:
        latex, _ = self.suma()
        # Lo que sobre (un ')' o ',' suelto) se muestra igual
        while self.actual().tipo != "FIN":
            latex += self.cursor() + self.avanzar().latex
            if self.actual().tipo != "FIN":
                latex += " " + self.suma()[0]
        return latex + self.cursor()


def _sin_parentesis(nodo) -> str:
    latex, interior = nodo
    return interior if interior is not None else latex


def texto_a_latex(texto: str, cursor=None, decimal_coma: bool = False):
    """Devuelve (latex, incompleta). incompleta es True si hay algún □.

    cursor es la posición (índice en el texto) donde dibujar el cursor.
    decimal_coma lee '2,5' como un número (para las celdas de las tablas).
    """
    traductor = _Traductor(_tokenizar(texto, cursor, decimal_coma))
    latex = traductor.todo()
    return latex, traductor.huecos > 0
