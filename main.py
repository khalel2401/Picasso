import tkinter as tk


def leer_tablero(archivo):
    tablero = []
    for linea in archivo:
        fila = list(linea.strip())
        tablero.append(fila)
    return tablero


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

def crear_tablero(tablero, FILAS, COLUMNAS):
    ventana = tk.Tk()
    ventana.title("Tablero")

    pistas_filas = [contar_bloques_negros(fila[:COLUMNAS]) for fila in tablero[:FILAS]]
    pistas_columnas = [
        contar_bloques_negros([tablero[fila][columna] for fila in range(FILAS)])
        for columna in range(COLUMNAS)
    ]
    max_pistas_filas = max((len(pista) for pista in pistas_filas), default=0)
    max_pistas_columnas = max((len(pista) for pista in pistas_columnas), default=0)
    origen_x = max_pistas_filas * TAMANO_CASILLA
    origen_y = max_pistas_columnas * TAMANO_CASILLA

    tablero_canvas = tk.Canvas(
        ventana,
        width=origen_x + COLUMNAS * TAMANO_CASILLA,
        height=origen_y + FILAS * TAMANO_CASILLA,
        highlightthickness=0,
    )
    tablero_canvas.pack(padx=10, pady=10)

    for fila, pista in enumerate(pistas_filas):
        for indice, cantidad in enumerate(pista):
            x = origen_x - (len(pista) - indice - 0.5) * TAMANO_CASILLA
            y = origen_y + (fila + 0.5) * TAMANO_CASILLA
            tablero_canvas.create_text(x, y, text=str(cantidad), font=("Arial", 8))

    for columna, pista in enumerate(pistas_columnas):
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
            color = "white" if tablero[fila][columna] == "0" else "black"

            tablero_canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="black",
                width=1,
            )

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

def main():
    select = ventana_inicial()
    print(select)
    archivo = open(f"tablero{select}.txt", "r")
    print(f"Archivo seleccionado: tablero{select}.txt")
    tablero = leer_tablero(archivo)
    archivo.close()
    FILAS = len(tablero)
    COLUMNAS = len(tablero[0]) if FILAS > 0 else 0
    crear_tablero(tablero, FILAS, COLUMNAS)


main()