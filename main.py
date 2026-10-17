import tkinter as tk
import Astrella as A


matriz_pistas_filas = []
matriz_pistas_columnas = []
tablero_canvas_actual = None

def leer_tablero(archivo):
    tablero = []
    for linea in archivo:
        fila = list(linea.strip())
        tablero.append(fila)
    return tablero

def comparar_fila(tablero, tablero_juego, i):
    for j in range(len(tablero[0])):
        if tablero[i][j] != tablero_juego[i][j]:
            return False
    return True

def comparar_columna(tablero, tablero_juego, j):
    for i in range(len(tablero)):
        if tablero[i][j] != tablero_juego[i][j]:
            return False
    return True

def onClick(event, tablero_juego, i, j, casilla, tablero):
    if tablero_juego == tablero:
        return

    if tablero_juego[i][j] == "0":
        tablero_juego[i][j] = "1"
        event.widget.itemconfig(casilla, fill="black")
    else:
        tablero_juego[i][j] = "0"
        event.widget.itemconfig(casilla, fill="white")
    print(f"Celda actualizada a: {tablero_juego[i][j]}")

    if tablero_juego == tablero:
        ventana_final()

def resolver_aestrella(matriz_pistas_filas, matriz_pistas_columnas, tablero_juego,tablero):
    solucion = A.aestrella(matriz_pistas_filas, matriz_pistas_columnas)
    if solucion is None:
        return

    solucion = [list(map(str, fila)) for fila in solucion]
    casillas = [
        item
        for item in tablero_canvas_actual.find_all()
        if tablero_canvas_actual.type(item) == "rectangle"
    ]

    tablero_juego[:] = solucion
    celdas = (celda for fila in solucion for celda in fila)
    for casilla, celda in zip(casillas, celdas):
        tablero_canvas_actual.itemconfig(
            casilla, fill="black" if celda == "1" else "white"
        )
    if tablero_juego == tablero:
        ventana_final()


TAMANO_CASILLA = 11


def contar_bloques_negros(celdas):
    bloques = []
    consecutivos = 0

    for celda in celdas:
        if celda != "0":
            consecutivos += 1
        elif consecutivos:
            bloques.append(consecutivos)
            consecutivos = 0

    if consecutivos:
        bloques.append(consecutivos)

    return bloques


def generar_pistas(tablero):
    global matriz_pistas_filas, matriz_pistas_columnas

    filas = len(tablero)
    columnas = len(tablero[0]) if filas else 0
    matriz_pistas_filas = [
        contar_bloques_negros(fila[:columnas]) for fila in tablero
    ]
    matriz_pistas_columnas = [
        contar_bloques_negros([tablero[fila][columna] for fila in range(filas)])
        for columna in range(columnas)
    ]
    return matriz_pistas_filas, matriz_pistas_columnas


def crear_tablero(tablero, tablero_juego, FILAS, COLUMNAS):
    global tablero_canvas_actual

    ventana = tk.Tk()
    ventana.title("Tablero")

    generar_pistas(tablero)
    max_pistas_filas = max((len(pista) for pista in matriz_pistas_filas), default=0)
    max_pistas_columnas = max((len(pista) for pista in matriz_pistas_columnas), default=0)
    origen_x = max_pistas_filas * TAMANO_CASILLA
    origen_y = max_pistas_columnas * TAMANO_CASILLA
    ancho_tablero = origen_x + COLUMNAS * TAMANO_CASILLA
    alto_tablero = origen_y + FILAS * TAMANO_CASILLA
    ancho_vista = min(ancho_tablero, ventana.winfo_screenwidth() - 100)
    alto_vista = min(alto_tablero, ventana.winfo_screenheight() - 180)

    marco_tablero = tk.Frame(ventana)
    marco_tablero.pack(padx=10, pady=10, fill="both", expand=True)
    marco_tablero.rowconfigure(0, weight=1)
    marco_tablero.columnconfigure(0, weight=1)
    tablero_canvas = tk.Canvas(
        marco_tablero,
        width=ancho_vista,
        height=alto_vista,
        highlightthickness=0,
        scrollregion=(0, 0, ancho_tablero, alto_tablero),
    )
    tablero_canvas_actual = tablero_canvas
    barra_horizontal = tk.Scrollbar(
        marco_tablero, orient="horizontal", command=tablero_canvas.xview
    )
    barra_vertical = tk.Scrollbar(
        marco_tablero, orient="vertical", command=tablero_canvas.yview
    )
    tablero_canvas.configure(
        xscrollcommand=barra_horizontal.set,
        yscrollcommand=barra_vertical.set,
    )
    tablero_canvas.grid(row=0, column=0, sticky="nsew")
    barra_vertical.grid(row=0, column=1, sticky="ns")
    barra_horizontal.grid(row=1, column=0, sticky="ew")

    for fila, pista in enumerate(matriz_pistas_filas):
        for indice, cantidad in enumerate(pista):
            x = origen_x - (len(pista) - indice - 0.5) * TAMANO_CASILLA
            y = origen_y + (fila + 0.5) * TAMANO_CASILLA
            tablero_canvas.create_text(x, y, text=str(cantidad), font=("Arial", 8))

    for columna, pista in enumerate(matriz_pistas_columnas):
        for indice, cantidad in enumerate(pista):
            x = origen_x + (columna + 0.5) * TAMANO_CASILLA
            y = origen_y - (len(pista) - indice - 0.5) * TAMANO_CASILLA
            tablero_canvas.create_text(x, y, text=str(cantidad), font=("Arial", 8))

    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            x1 = origen_x + columna * TAMANO_CASILLA
            y1 = origen_y + fila * TAMANO_CASILLA
            x2 = x1 + TAMANO_CASILLA
            y2 = y1 + TAMANO_CASILLA
            color = "white"
            casilla = tablero_canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="black",
                width=1,
            )
            tablero_canvas.tag_bind(
                casilla,
                "<Button-1>",
                lambda event, i=fila, j=columna, item=casilla: onClick(
                    event, tablero_juego, i, j, item, tablero
                ),
            )

    tk.Button(
        ventana,
        text="Resolver",
        command=lambda: resolver_aestrella(matriz_pistas_filas, matriz_pistas_columnas,tablero_juego,tablero)
    ).pack(pady=10)

    ventana.mainloop()


def ventana_inicial():
    ventana = tk.Tk()
    ventana.title("Seleccionar tablero")
    seleccion = tk.IntVar(value=0)

    def elegir_tablero(numero):
        seleccion.set(numero)
        ventana.destroy()

    for numero in range(1, 4):
        tk.Button(
            ventana,
            text=f"Tablero {numero}",
            command=lambda numero=numero: elegir_tablero(numero),
        ).pack(padx=20, pady=10, fill="x")

    ventana.mainloop()
    return seleccion.get()

def ventana_final():
    ventana = tk.Toplevel()
    ventana.title("¡Felicidades!")
    tk.Label(ventana, text="GANASTE!!!!1!!1!!!!!").pack(padx=20, pady=10)
    tk.Button(ventana, text="Cerrar").pack(pady=10)

def main():
    select = ventana_inicial()
    print(select)
    archivo = open(f"tablero{select}.txt", "r")
    print(f"Archivo seleccionado: tablero{select}.txt")
    tablero = leer_tablero(archivo)
    archivo.close()
    FILAS = len(tablero)
    COLUMNAS = len(tablero[0]) if FILAS > 0 else 0
    tablero_juego = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
    for i in range(FILAS):
            for j in range(COLUMNAS):
                tablero_juego[i][j] = "0"  
    crear_tablero(tablero, tablero_juego, FILAS, COLUMNAS)

main()