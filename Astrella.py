import heapq
import Heuristica as H

def aestrella(pistas_fila, pistas_columna):
    total_filas = len(pistas_fila)
    total_columnas = len(pistas_columna)

    candidatos_filas = [
        H.patrones(total_columnas, pista) 
        for pista in pistas_fila
    ]

    candidatos_columnas = [
        H.patrones(total_filas, pista)
        for pista in pistas_columna
    ]

    estado_inicial = ()
    tope = [(total_filas, 0, estado_inicial)]

    visited = {estado_inicial}
    contado = 1

    while tope:
        prioridad, _, estado = heapq.heappop(tope)

        if len(estado) == total_filas:
            return estado
        
        for sucesor in H.generar_sucesores(estado, candidatos_filas, candidatos_columnas):
            if sucesor in visited:
                continue

            visited.add(sucesor)

            f = H.heuristica(sucesor, total_filas, candidatos_columnas)

            heapq.heappush(tope, (f, contado, sucesor))
            
    return None