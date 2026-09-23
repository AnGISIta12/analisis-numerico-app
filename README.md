# Proyecto Numérico

    pip install -r requirements.txt
    streamlit run main.py

Estructura:

    main.py                          # conecta todo y arranca la app
    algoritmos/                      # lógica pura (sin interfaz)
      funciones.py                   # texto -> función y derivada (sympy);
                                     # acepta 2x, x^2, sen, ln, π, √ ...
      raices/
        biseccion.py                 # scipy.optimize.bisect
        posicion_falsa.py            # a mano (SciPy no lo trae)
        punto_fijo.py                # scipy.optimize.fixed_point (method="iteration")
        newton.py                    # scipy.optimize.newton con fprime
        secante.py                   # scipy.optimize.newton sin fprime, con x1
      sistemas_lineales/
        validacion.py                # A cuadrada, b del tamaño correcto, A no singular
        gauss.py                     # sympy (escalonada) + numpy.linalg.solve
        lu.py                        # sympy LUdecomposition (sin pivoteo)
        lup.py                       # scipy.linalg.lu / lu_factor / lu_solve
        gauss_seidel.py              # a mano (NumPy/SciPy no lo traen)
    interfaces/                      # pantallas; solo llaman a algoritmos/
      barra_lateral.py               # unidad -> método (compartida)
      notacion.py                    # texto -> LaTeX tal cual se escribe (con cursor y □)
      teclado.py                     # teclado matemático con cursor (raíces y sistemas)
      raices/
        entrada_funcion.py           # f(x) con el teclado y vista previa
        pantalla_<metodo>.py
      sistemas_lineales/
        componentes.py               # celdas de A|b con el teclado y cómo mostrar matrices
        pantalla_<metodo>.py

Para agregar un método: crea `algoritmos/<unidad>/<metodo>.py` y
`interfaces/<unidad>/pantalla_<metodo>.py`, añade el nombre en `UNIDADES`
de `barra_lateral.py` y la entrada en `PANTALLAS` de `main.py`.
Para una unidad nueva, lo mismo pero creando las dos carpetas.
