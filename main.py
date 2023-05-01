from simplex import simplex_m2f
from simplexmetodos import *
import pandas as pd
import numpy as np
import re

from input_simplex_estandar import *

r = input("Ingrese sus restricciones separando cada una con una coma: ")
res = r.split(",")

Z = input("Ingrese la función objetivo: ")

des = getDesigualdad(res)
print(des)

# Primer caso: encontrar más de 2 desigualdades
if len(des) > 1:
    simplex_m2f()
else:
    # Segundo caso: encontrar una desigualdad
    if des[0] == "<=":
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
        restricciones_ampliadas = agregar_holguras(res, des[0], VB)

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
        
    else:
        simplex_m2f()
