# se importa la libreria para usar ramdom
import random

#se crea una funcion que recibe una matriz la recorre completa e identifica el valor menor
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

#se crea ua funcion que recibe una matriz y la posicion de un valor menor y devuelve
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
#se crea una funcion que recibe una matriz y la posicion de un valor menor,
#aplicamos reduccion gaussiana y devuelve la matriz con los valores actualizados
#utilizando las funciones getValoresFilaColumna y getPosicionMenor
def reduccionGaussiana(matriz,posicion):
    #se crea una variable que almacena los valores de la fila y columna
    fila,columna = getValoresFilaColumna(matriz,posicion)
    #se crea una variable que almacena el valor menor
    menor = matriz[posicion[0]][posicion[1]]
    #se recorre la matriz
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            #se compara la posicion actual con la posicion del valor menor
            if i == posicion[0]:
                #si la posicion actual es igual a la posicion del valor menor se actualiza el valor de la matriz
                matriz[i][j] = matriz[i][j] - menor
            if j == posicion[1]:
                #si la posicion actual es igual a la posicion del valor menor se actualiza el valor de la matriz
                matriz[i][j] = matriz[i][j] + menor
    return matriz
# se crea una funcion que recibe una matriz y la agrega al final de un archivo csv si no existe el archivo lo crea si borrar los datos previos
def crearArchivo(matriz):
    #se crea un archivo csv
    archivo = open("matriz.csv","a")
    #se recorre la matriz
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            #se agrega la matriz al archivo
            archivo.write(str(matriz[i][j])+",")
        archivo.write("\n")
    archivo.write("\n")
    archivo.close()
    
#test de metodos
#-------------------------------
#se crea una matriz de prueba de n dimesiones 4x6 con numeros aleatorios y distintos
matriz = [[random.randint(1,100) for i in range(6)] for j in range(4)]
#se imprime la matriz
print(matriz)
#se crea un archivo csv con la matriz
crearArchivo(matriz)
#se imprime la posicion del valor menor|
print(getPosicionMenor(matriz))
#se imprime los valores de la fila y columna
print(getValoresFilaColumna(matriz,getPosicionMenor(matriz)))
#se imprime la matriz con reduccion gaussiana
print(reduccionGaussiana(matriz,getPosicionMenor(matriz)))
#se agrega la nueva matriz al archivo csv
crearArchivo(reduccionGaussiana(matriz,getPosicionMenor(matriz)))

#-------------------------------