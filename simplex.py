import re

def getDesigualdad(restricciones:list) -> list:
    patron = re.compile(">=|<=")
    desigualdad = []

    for r in restricciones:
        match = patron.search(r)
        if match.group() not in desigualdad:
            desigualdad.append(match.group())

    return desigualdad

def simplex_estandar():
    print("Estándar")
    return None

def simplex_m2f():
    print("2 Fases")
    return None

# Identificar variables con sus coeficientes (Solo era una prueba)
patron = re.compile("\-{0,1}\s{0,1}\d{0,}x{1}\d{1}")