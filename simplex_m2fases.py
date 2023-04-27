import re
import pandas as pd
import numpy as np

#restricciones = 60x1 + 60x2 >= 300, 12x1 + 6x2 >= 36,10x1 + 30x2 >= 90,x1 >= 0, x2 >= 0

# funcion que amplia las restricciones segun sea el caso 
def ampliar_restricciones():
    
    restricciones_ampliadas = []
    patron = r'[<=>]='

    #introducir las restricciones separadas por coma
    restricciones = input("Introducir las restricciones separadas por coma: ")
    restricciones = [r.strip() for r in restricciones.split(",")]
    
    for i, restriccion in enumerate(restricciones):
        operador = re.findall(patron, restriccion)
        
        # En caso de que no encuentre ningun operador se termina el proceso
        if len(operador) == 0:
            print(f"No se encontró operador en la restricción {restriccion}")
            break
            
        #se separa la restriccion 
        res_izq, res_der = restriccion.split(operador[0])
        res_der = int(res_der.strip())
        
        # Se crea la variable correspondiente según el tipo de variable
        if "<=" in restriccion:
            var_holgura = f"h{i+1}"
            restriccion_ampliada = f"{res_izq} + {var_holgura} = {res_der}"
        elif ">=" in restriccion:
            var_exceso = f"e{i+1}"
            var_artificial = f"a{i+1}"
            restriccion_ampliada = f"{res_izq} - {var_exceso} + {var_artificial} = {res_der}"
        
        #agregar a la lista de restricciones ampliadas
        restricciones_ampliadas.append(restriccion_ampliada)

    return restricciones_ampliadas
        
#===========================================================================================================================
#===========================================================================================================================

# funcion que obtiene el nombre de las variables ( recibe una lista de restricciones )
def obtener_variables(restricciones):

    # lista para almacenar los nombres de variables
    variables = []
    patron = r'\b[a-zA-Z]+\d+\b'
    
    # buscar nombres de variables en cada restricción
    for restriccion in restricciones:
        # utilizar re.findall() para buscar nombres de variables en la restricción
        nombres_variables = re.findall(patron, restriccion)
        # agregar los nombres de variables encontrados a la lista de variables
        for nombre in nombres_variables:
            if nombre not in variables:
                variables.append(nombre)
                
    #ordenar las variables
    variables.sort(key=lambda x: x[1:] if len(x) > 1 else x)
    
    #agregar Z y LD en sus posiciones
    variables.insert(0, "Z")
    variables.append("LD")
    
    return variables
   
#===========================================================================================================================
#===========================================================================================================================
#===========================================================================================================================

# funcion que obtiene los valores numericos de las restricciones ( recibe listas de las restricciones y nombre de las variables ) 
def obtener_coeficientes(restricciones, variables):
    patron = r'(-?\d*(?:\.\d+)?)\s*([a-zA-Z]+[\d]*)'
    coeficientes = []
    dicc_variables = {}

    # Crear un diccionario con el orden de las variables
    for i, variable in enumerate(variables):
        dicc_variables[variable] = i

    for restriccion in restricciones:
        lista_coeficientes = [0] * len(variables)
        tuplas_coeficientes = re.findall(patron, restriccion)

        for tupla in tuplas_coeficientes:   
            if tupla[0] == '':                  # En caso de que no exista un coeficiente numerico se asume que es 1, 
                coeficiente = 1
            elif tupla[0] == '-':               # si el coeficiente es un guión, se asume que es -1, de lo contrario,
                coeficiente = -1
            else:
                coeficiente = float(tupla[0])   # se asigna el valor numérico que tenga asociado

            # se ordenan los valores segun el orden de las variables previamente dadas
            nombre_variable = tupla[1]
            if nombre_variable in dicc_variables:
                posicion_variable = dicc_variables[nombre_variable]
                lista_coeficientes[posicion_variable] = coeficiente

        # se agrega el valor del lado derecho a la lista de coeficientes
        constante = float(restriccion.split('=')[1].strip())
        lista_coeficientes[-1] = constante
        coeficientes.append(lista_coeficientes)

    # se transforman los ceros a coma flotante
    for i in range(len(coeficientes)):
        for j in range(len(variables)):
            if coeficientes[i][j] == 0:
                coeficientes[i][j] = 0.0

    return coeficientes

#===========================================================================================================================

#funcion que calcula cuales son las columnas con variables artificiales ( recibe una lista del nombre de las variables )
def obtener_variables_artificiales(variables):
    variables_artificiales = [var for var in variables if var.startswith('a')]
    return variables_artificiales

#===========================================================================================================================.

# funcion que obtiene la columna pivote en base al nombre de esta
def obtener_columna_pivote(matriz,nombre_columna):
    columna = matriz.loc[:, nombre_columna]     # selecciona la columna con el nombre asignado( a1,a2,x1,x2,etc )
    return columna

#===========================================================================================================================

# funcion que crea una matriz tipo dataframe de pandas
def crear_matriz():
    restricciones = ampliar_restricciones()
    variables = obtener_variables(restricciones)

    #restricciones = ['-Z + a1 + a2 + a3 = 0','60x1 + 60x2  -e1 + a1 = 300', '12x1 + 6x2  - e2 + a2 = 36', '10x1 + 30x2  - e3 + a3 = 90']
    #variables = ['Z', 'e1', 'a1', 'x1', 'e2', 'a2', 'x2', 'e3', 'a3', 'LD']
    z = '-Z + a1 + a2 + a3 = 0'
    restricciones.insert(0,z)           #se agrega la funcion z a la lista de restricciones  (esto es temporal)

    coeficientes = obtener_coeficientes(restricciones,variables)

    # formar los nombres para las filas
    filas = obtener_variables_artificiales(variables)
    filas.insert(0,'Z')

    # crear dataframe con los datos
    matriz = pd.DataFrame(coeficientes, columns=variables, index=filas)
    print(matriz)

    return matriz

#===========================================================================================================================
#restricciones = 60x1 + 60x2 >= 300, 12x1 + 6x2 >= 36,10x1 + 30x2 >= 90,x1 >= 0, x2 >= 0

# restricciones = xeA + xoA >= 40, xeB + xoB >= 70, 2xeA + 2xoA <= xeB + xoB, xeA + xeB <= 180, xoA + xoB <= 45, xij >= 0
# restricciones = xeA + xoA >= 40, xeB + xoB >= 70, xeA + xeB <= 180, xoA + xoB <= 45, xij >= 0
# restricciones = x1 + x2 >= 40, x3 + x4 >= 70, x1 + x3 <= 180, x2 + x4 <= 45, x5 >= 0
#variables = ['Z', 'e1', 'a1', 'x1', 'e2', 'a2', 'x2', 'e3', 'a3', 'LD']

#===========================================================================================================================

# funcion que calcula la columna pivote ( recibe la matriz y el nombre de la columna que se quiere tratar) 
def seleccionar_pivote(matriz,columna):

    LD = matriz.iloc[:, -1]                 # seleccionar columna del lado derecho
    div = []                                # lista para guardar las divisiones

    col = obtener_columna_pivote(matriz,columna)

    # ciclo para dividir el lado derecho por la columna pivote 
    for i in range(len(LD)):
        if(col[i]!=float(0) and LD[i]>float(0)):
            div.append((LD[i] / col[i],i))      # añadir a la lista las divisiones junto con su posicion 
    
    print(div)
    menor = min([tupla[0] for tupla in div])   #obtener el valor minimo
    posicion = [tupla[1] for tupla in div if tupla[0] == menor][0]  #obtener la posicion  del valor minimo

    pivote = [menor,posicion]       # formar tupla con el pivote y la fila a la que pertenece

    return pivote
            
#===========================================================================================================================

# funcion reduccion gaussiana 
#def gauss(matriz,columna):
 #   col_artificiales = obtener_variables_artificiales(variables)
  # return 0

matriz = crear_matriz()



