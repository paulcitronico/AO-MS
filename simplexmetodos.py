# se importa la libreria para usar ramdom
import random

#se crea una funcion que recorre la primera fila de la matriz menos uno
#y retorna el valor mas negativo
def columnaPivote(matriz):
    #se crea una lista con los valores de la primera fila de la matriz
    lista = matriz[0]
    #se crea una variable para guardar el valor mas negativo
    menor = 0
    #se recorre la lista
    for i in range(len(lista)-1):
        #se verifica si el valor es mas negativo que el anterior
        if lista[i] < lista[menor]:
            #se guarda el valor mas negativo
            menor = i
    #se retorna el valor mas negativo
    return menor

#se crea una funcion que recibe una matriz y una posicion
# y retorna la fila pivote
def filaPivote(matriz,posicion):
    #la untima comuna de la matriz desde la posicion 1 hasta el final se divide 
    #por la columna de la posicion recibida si se divide en 0
    # entonces el valor agregado es 0, y se guarda en una lista
    lista = [matriz[i][-1]/matriz[i][posicion] if matriz[i][posicion] != 0 else 0 for i in range(1,len(matriz))]
    #se retorna el menos valor de la lista +1 distinto de cero
    return lista.index(min([i for i in lista if i != 0 and i>0]))+1
    
#se crea una funcion que recibe una matriz,
#una posicion de la fila pivote y una posicion de la columna pivote
#se realiza operacion en fila pivote
def opFilapivote(matriz,posicionFila,posicionColumna):
    #se almacena en una variable el valor de la posicion pivote
    pivote = matriz[posicionFila][posicionColumna]
    #print("valor pivote: "+str(pivote))
    #se divide la fila pivote por el valor pivote
    matriz[posicionFila] = [matriz[posicionFila][i]/pivote for i in range(len(matriz[posicionFila]))]
    return matriz

#se crea una funcion llamada opOtrasfilas que recibe una matriz,
#una posicion de la fila pivote y una posicion de la columna pivote
#se realiza operacion en otras filas sin modificar la fila pivote
def opOtrasfilas(matriz,posicionFila,posicionColumna):
    #se recorre la matriz
    for i in range(len(matriz)):
        #se verifica si la posicion es diferente de la fila pivote
        if i != posicionFila:
            #se almacena en una variable el valor de la posicion pivote
            pivote = matriz[i][posicionColumna]
            #se recorre la fila pivote
            for j in range(len(matriz[i])):
                #se realiza la operacion en la fila pivote
                matriz[i][j] = matriz[i][j] - (pivote * matriz[posicionFila][j])
    return matriz



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
#se crea una matriz del ejemplo puertas y ventanas
matriz = [[1,-30000,-50000,0,0,0,0],[0,1,0,1,0,0,4],[0,0,2,0,1,0,12],[0,3,2,0,0,1,18]]
#ejemplo matriz perfumeria
#matriz= [[1,-2,-2,0,0,0,0,0],[0,1,0,1,0,0,0,45],[0,0,1,0,1,0,0,100],[0,1,3,0,0,1,0,80],[0,2,1,0,0,0,1,100]]

#se crea un archivo csv con la matriz inicial
crearArchivo(matriz)
print(matriz)
print("columna pivote: "+str(columnaPivote(matriz)))
print("fila pivote: "+str(filaPivote(matriz,columnaPivote(matriz))))
    
#se crea un archivo csv con la matriz reducida
#crearArchivo(opFilapivote(matriz,filaPivote(matriz,columnaPivote(matriz)),columnaPivote(matriz)))
#matriz2=opOtrasfilas(opFilapivote(matriz,filaPivote(matriz,columnaPivote(matriz)),columnaPivote(matriz)),filaPivote(matriz,columnaPivote(matriz)),columnaPivote(matriz))
#crearArchivo(matriz2)

#matriz3=opOtrasfilas(opFilapivote(matriz2,filaPivote(matriz2,columnaPivote(matriz2)),columnaPivote(matriz2)),filaPivote(matriz2,columnaPivote(matriz2)),columnaPivote(matriz2))
#crearArchivo(matriz3)
#crearArchivo(opFilapivote(matriz3,filaPivote(matriz3,columnaPivote(matriz3)),columnaPivote(matriz3)))
#matriz4=opOtrasfilas(opFilapivote(matriz3,filaPivote(matriz3,columnaPivote(matriz3)),columnaPivote(matriz3)),filaPivote(matriz3,columnaPivote(matriz3)),columnaPivote(matriz3))
#crearArchivo(matriz4)

#se crea un bucle que termina cuando los valores de la primera fila de la matriz son >= 0
#en cada iteracion se crea un archivo csv con la matriz reducida
while min(matriz[0]) < 0:
    matriz = opOtrasfilas(opFilapivote(matriz,filaPivote(matriz,columnaPivote(matriz)),columnaPivote(matriz)),filaPivote(matriz,columnaPivote(matriz)),columnaPivote(matriz))
    crearArchivo(matriz)
    print(matriz)
    print("columna pivote: "+str(columnaPivote(matriz)))
    print("fila pivote: "+str(filaPivote(matriz,columnaPivote(matriz))))
    print("matriz reducida")
    print(matriz)
    print("-------------------------------")
#-------------------------------