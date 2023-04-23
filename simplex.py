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
patron = re.compile("(\-{0,1}\s{0,}\d{0,}[a-zA-Z]{1}\d{1})|[zZ]")

# se importa la libreria para usar ramdom
import random

#se crea una funcion que recibe un dataframe la recorre completa e identifica el valor menor
#y devuelve la posicion de la fila y columna del valor menor
def getPosicionMenor(matriz):
    #se crea una variable que almacena el valor menor
    menor = matriz[0][0]
    #se crea una variable que almacena la posicion del valor menor
    posicion = [0,0]
    #se recorre la matriz
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            #se compara el valor de la posicion actual con el valor menor
            if matriz[i][j] < menor:
                #si el valor actual es menor se actualiza el valor menor y la posicion
                menor = matriz[i][j]
                posicion = [i,j]
    return posicion

#se crea ua funcion que recibe un dataframe y la posicion de un valor menor y devuelve
#retorna todos los valores de la fila y columna
def getValoresFilaColumna(matriz,posicion):
    #se crea una variable que almacena los valores de la fila
    fila = []
    #se crea una variable que almacena los valores de la columna
    columna = []
    #se recorre la matriz
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            #se compara la posicion actual con la posicion del valor menor
            if i == posicion[0]:
                #si la posicion actual es igual a la posicion del valor menor se almacena el valor en la fila
                fila.append(matriz[i][j])
            if j == posicion[1]:
                #si la posicion actual es igual a la posicion del valor menor se almacena el valor en la columna
                columna.append(matriz[i][j])
    return fila,columna
#test de metodos
#-------------------------------
# se prueba el metoodo getposicionmenor
#se crea una matriz de prueba de n dimesiones 4x6 con numeros aleatorios y distintos
matriz = [[random.randint(1,100) for i in range(6)] for j in range(4)]
#se imprime la matriz
print(matriz)
#se imprime la posicion del valor menor
print(getPosicionMenor(matriz))
#se imprime los valores de la fila y columna
print(getValoresFilaColumna(matriz,getPosicionMenor(matriz)))

#-------------------------------