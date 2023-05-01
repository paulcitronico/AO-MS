# Módulo con métodos relacionados a la entrada de datos
import re
import pandas as pd
from simplexmetodos import *

terminos = re.compile("(\-{0,1}\s{0,}\d{0,}[a-zA-Z]{1}\d{1})|[zZ]") # Validar términos, ejemplo X1, 3x2, -4x1, etc.
symbol = re.compile("[a-zA-Z]\d{0,}") #Validar variables
digit = re.compile("(^\W[0-9]{1,})|(^[0-9]{1,})|(^\-{1}\W{0,}[0-9]{1,})|(\d{1,}\+{1,1}\d{1,})") #Validar digitos
ld = re.compile("={1}\W{0,}(\d{1,})|(\d{1,}\+{1,1}\d{1,})") # Validar lado derecho

def getDesigualdad(restricciones:list) -> list:
    patron = re.compile(">=|<=")
    desigualdad = []

    for r in restricciones:
        match = patron.search(r)
        if match.group() not in desigualdad:
            desigualdad.append(match.group())

    return desigualdad

"""
Descripción:
Buscar variables para agregarlas a la columna del dataframe y buscar coeficientes para armar la matriz.
Params:
lista -> Lista con restricciones ya sea estándar o ampliadas.
columns -> Lista de columnas del dataframe a la cual se incorporan las variables que no existan en ella.
"""
def search_variables_y_coeficientes(lista:list, columns:list):
    coeficientes = {}
    for i in lista:
        # Buscar variables y agregarlas a la columna del dataframe
        sym = symbol.search(i.group())
        if sym.group() not in columns:
            columns.append(sym.group())
        # Buscar coeficientes
        search = digit.search(i.group())
        if search == None: # Si no encuentra coeficientes, reemplazar por -1 o 1, dependiendo del signo que acompañe a la variable.
            if "-" in i.group():
                coeficientes[sym.group()] = -1
            else:
                coeficientes[sym.group()] = 1
        else:
            coeficientes[sym.group()] = search.group()

    return coeficientes, columns

def agregar_holguras(res:list, desigualdad:str, VB:list):
    # Ampliar restricciones (con holguras)
    restricciones_ampliadas = []
    for r in range(len(res)):
        split = res[r].split(desigualdad)
        holgura = "h{}".format(r+1)
        # Agregar la variable de holgura a la lista de variables básicas
        if holgura not in VB:
            VB.append(holgura)
        restriccion_ampliada = "{}+ {} ={}".format(split[0],holgura,split[1])
        restricciones_ampliadas.append(restriccion_ampliada)
    return restricciones_ampliadas

def limpiar_dataframe(df:pd.DataFrame):
    # Limpiar valores NaN del dataframe y transformar a un tipo de dato numérico
    for i in range(len(df)):
        df.loc[i] = df.loc[i].fillna(0)
        df.loc[i] = pd.to_numeric(df.loc[i])
    return df

def armar_matriz(Z, res, desigualdad):
    VB = []
    columns = []
    # Generar la matriz con los coeficientes para generar el dataframe
    matriz_coeficientes = []
    # Necesitamos encontrar los términos de la función objetivo para posteriormente ampliarla.
    z = list(terminos.finditer(Z))
    # Agregar el término Z a la lista de variables básicas
    VB.append(z[0].group())
    template = ""
    # Iteramos cada término de la función objetivo
    for e in range(1, len(z)):
        template += "-{} ".format(z[e].group())

    # Con operaciones de strings, armamos la función objetivo ampliado
    z_ampliado = z[0].group() + template + "= 0"
    # De la función objetivo ampliada, reemplazamos los espacios en blanco por una cadena vacía
    z_ampliado = re.sub("\s", "", z_ampliado)
    # En caso de encontrar doble signo negativo, reemplazar por un +
    z_ampliado = re.sub("--","+",z_ampliado)
    print("====================Función Objetivo Ampliada====================")
    print(z_ampliado)

    # Volvemos a generar una lista con los términos de la función objetivo ampliada
    c_z_ampliado = list(terminos.finditer(z_ampliado))

    # Buscar los coeficientes de la función objetivo ampliada
    coeficientes, columns = search_variables_y_coeficientes(c_z_ampliado, columns)

    # Incorporar los coeficientes a la matriz
    matriz_coeficientes.append(coeficientes)

    # como son restricciones de menor o igual, se agregan variables de holgura a las restricciones
    # Además de agregar las variables de holgura a la lista de variables básicas
    restricciones_ampliadas = agregar_holguras(res, desigualdad, VB)

    # Para cada restricción ampliada
    for f in restricciones_ampliadas:
        # Encontrar cada término
        t = terminos.finditer(f)
        s = list(t)
        # Separar coeficientes para agregarlos a la matriz, e incorporar
        # las variables restantes a las columnas del dataframe
        coeficientes, columns = search_variables_y_coeficientes(s,columns)
        # Determinar el lado derecho y agregarlo.
        lado_derecho = ld.search(f)
        l_d = digit.search(lado_derecho.group()[1:])
        print(l_d.group())
        coeficientes["LD"] = l_d.group()
        matriz_coeficientes.append(coeficientes)
    columns.append("LD")

    # Armar la matriz
    df = pd.DataFrame(data = matriz_coeficientes, columns=columns)
    df = limpiar_dataframe(df)

    df.index = VB
    print("Tablero Inicial")
    print(df)

    dataframes = [df]
    #matriz principal
    matriz=df.to_numpy()
        #se crea un archivo csv con la matriz inicial
        #crearArchivo(matriz)
        #print(matriz)
        #print("columna pivote: "+str(columnaPivote(matriz)))
        #print("fila pivote: "+str(filaPivote(matriz,columnaPivote(matriz))))
        #se crea un bucle que termina cuando los valores de la primera fila de la matriz son >= 0
        #en cada iteracion se crea un archivo csv con la matriz reducida
        
    pasos = 1
    while min(matriz[0]) < 0:
        matriz, df_matriz = opOtrasfilas(opFilapivote(matriz,filaPivote(matriz,columnaPivote(matriz)),columnaPivote(matriz)),filaPivote(matriz,columnaPivote(matriz)),columnaPivote(matriz), VB, columns)
        print("Iteración número: {}".format(pasos))
        print(df_matriz)
        dataframes.append(df_matriz)
        pasos += 1
            #crearArchivo(matriz)
            #print(matriz)
            #print("columna pivote: "+str(columnaPivote(matriz)))
            #print("fila pivote: "+str(filaPivote(matriz,columnaPivote(matriz))))
            #print("matriz reducida")
            #print(matriz)
            #print("-------------------------------")
    # Crear archivo con cada iteración
    df_1 = pd.concat(dataframes)
    df_1.to_csv("./data1.csv")
    return dataframes