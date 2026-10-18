estado_inicial = ()

def patrones(lenght, pistas):
    patrones = []

    if not pistas:
            return [tuple([0] * lenght)]
    
    def generar_patrones(indice, posicion, bits):
        if indice == len(pistas):
            patron = bits + ['0'] * (lenght - len(bits))
            patrones.append(tuple(patron))
            return

        restantes = pistas[indice:]
        minimo = sum(restantes) + len(restantes) - 1
        maximo = lenght - minimo

        for espacio in range(posicion, maximo+1):
            nuevos_bits = bits + ['0'] * (espacio - len(bits))
            nuevos_bits += ['1'] * pistas[indice]

            if indice < len(pistas) - 1:
                nuevos_bits += ['0']
                generar_patrones(
                    indice + 1,
                    espacio + pistas[indice] + 1,
                    nuevos_bits
                )
            else:
                generar_patrones(
                    indice + 1, espacio + pistas[indice], nuevos_bits
                )

    generar_patrones(0, 0, [])
    return patrones

def columnas_validas(estado, candidatos_columnas):
    filas_asignadas = len(estado)

    for columna, candidatos in enumerate(candidatos_columnas):
        posible = any(
            all(
                patron[fila] == estado[fila][columna]
                for fila in range(filas_asignadas)
            )
            for patron in candidatos
        )

        if not posible:
            return False
    return True

def generar_sucesores(estado, candidatos_filas, candidatos_columnas):
    indice_fila = len(estado)

    if indice_fila >= len(candidatos_filas):
        return []

    sucesores = []

    for patron in candidatos_filas[indice_fila]:
        nuevo_estado = estado + (patron,)

        if columnas_validas(nuevo_estado, candidatos_columnas):
            sucesores.append(nuevo_estado)
    return sucesores

def costo(estado):
    return len(estado)

def es_estado_final(estado, total_filas):
    return total_filas - len(estado)

def posibilidades_columnas(estado, candidatos_columnas):
    filas_asignadas = len(estado)
    posibilidades = 0

    for columna, candidatos in enumerate(candidatos_columnas):
        posibles = [
            patron
            for patron in candidatos
            if all(
                patron[fila] == estado[fila][columna]
                for fila in range(filas_asignadas)
            )
        ]
        posibilidades += len(posibles)

    return posibilidades

def heuristica(estado, total_filas, candidatos_columnas):
    return es_estado_final(estado, total_filas) + posibilidades_columnas(estado, candidatos_columnas)
