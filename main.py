from ctypes import sizeof
import tkinter as tk


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
        ventana_final(event.widget.winfo_toplevel())


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
    filas = len(tablero)
    columnas = len(tablero[0]) if filas else 0
    return {
        "filas": [
            contar_bloques_negros(fila[:columnas]) for fila in tablero
        ],
        "columnas": [
            contar_bloques_negros([tablero[fila][columna] for fila in range(filas)])
            for columna in range(columnas)
        ],
    }


def crear_tablero(tablero, tablero_juego, FILAS, COLUMNAS):
    ventana = tk.Tk()
    ventana.title("Tablero")

    pistas = generar_pistas(tablero)
    pistas_filas = pistas["filas"]
    pistas_columnas = pistas["columnas"]
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

def ventana_final(ventana_juego):
    ventana = tk.Toplevel(ventana_juego)
    ventana.title("¡Felicidades!")
    tk.Label(ventana, text="GANASTE!!!!1!!1!!!!!").pack(padx=20, pady=10)
    tk.Button(ventana, text="Cerrar", command=ventana_juego.destroy).pack(pady=10)

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