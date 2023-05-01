import re
import pandas as pd
import numpy as np
from decimal import Decimal, getcontext


#restricciones = 60x1 + 60x2 >= 300, 12x1 + 6x2 >= 36,10x1 + 30x2 >= 90

# funcion que amplia las restricciones segun sea el caso 
def ampliar_restricciones():
    
    restricciones_ampliadas = []
    patron = r'[<=>]='      # detecta los operadores <=,>=,=

    #introducir las restricciones separadas por coma
    restricciones = input("Introducir las restricciones separadas por coma: ")
    #fz = input("Introducir la funcion Z: ")
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
    patron = r'[+\-*/]?[a-zA-Z]+\d*[+\-*/]?'    # detecta variables que empiezan con una letra seguida por cero o más dígitos y que tienen un operador matemático a la derecha o a la izquierda     
    
    # buscar nombres de variables en cada restricción
    for restriccion in restricciones:
        nombres_variables = re.findall(patron, restriccion)     # utilizar re.findall() para buscar nombres de variables en la restricción
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
    patron = r'(-?\d*(?:\.\d+)?)\s*([a-zA-Z]+[\d]*)'    # detecta los coeficientes y variables de la restriccion ( incluye negativos )
    coeficientes = []
    dicc_variables = {}

    # Crear un diccionario con el orden de las variables
    for i, variable in enumerate(variables):
        dicc_variables[variable] = i

    for restriccion in restricciones:
        lista_coeficientes = [0] * len(variables)               # lista para guardar los coeficientes
        tuplas_coeficientes = re.findall(patron, restriccion)   # busca con re.findall y crea las tuplas con los valores numericos(coeficientes)

        for tupla in tuplas_coeficientes:   
            if tupla[0] == '':                             # En caso de que no exista un coeficiente numerico se asume que es 1, 
                coeficiente = 1
            elif tupla[0] == '-':                          # si el coeficiente es un guión, se asume que es -1, de lo contrario,
                coeficiente = -1
            else:
                coeficiente = float(tupla[0])              # se asigna el valor numérico que tenga asociado

            # se ordenan los valores segun el orden de las variables previamente dadas
            nombre_variable = tupla[1]
            if nombre_variable in dicc_variables:                           # si existe el nombre de la variable dentro del diccionario previamente creado
                posicion_variable = dicc_variables[nombre_variable]     
                lista_coeficientes[posicion_variable] = coeficiente         # se agrega a la lista de coeficientes el del coeficiente actual

        # se agrega el valor del lado derecho a la lista de coeficientes
        constante = float(restriccion.split('=')[1].strip())                #se separa la constante por el simbolo =
        lista_coeficientes[-1] = constante                                  # busca el ultimo valor de la lista (la constante)
        coeficientes.append(lista_coeficientes)                             # añade este valor a la lista de coeficientes

    # se transforman los ceros a coma flotante
    for i in range(len(coeficientes)):
        for j in range(len(variables)):
            if coeficientes[i][j] == 0:
                coeficientes[i][j] = 0.0

    return coeficientes

#===========================================================================================================================

#funcion que calcula cuales son las columnas con variables artificiales ( recibe una lista del nombre de las variables )
def seleccionar_variables_artificiales(variables,nombre_variable):
    variables_artificiales = [var for var in variables if var.startswith(nombre_variable)]  # busca dentro de la lista de variables la que comienze con la letra asignada
    return variables_artificiales

# funcion que obtiene las variables segun su tipo (letra con que comienza a,e,h,x) ( recibe la matriz )
def seleccionar_variables_por_nombre(matriz,nombre_variable):
    variables = matriz.columns                                                              # obtiene el nombre de las columnas de la matriz
    variables_artificiales = [var for var in variables if var.startswith(nombre_variable)]  # busca dentro de la lista de variables la que comienze con la letra asignada
    return variables_artificiales

#===========================================================================================================================.

# funcion que obtiene una columna en base al nombre de esta
def seleccionar_columna(matriz,nombre_columna):
    columna = matriz.loc[:, nombre_columna]     # selecciona la columna con el nombre asignado( a1,a2,x1,x2,etc )
    return columna

# funcion que obtiene una fila en base al numero de esta
def seleccionar_fila(matriz,pos_fila):
    nombre_fila = matriz.index[pos_fila]    #busca el nombre asignado en base a su posicion
    fila = matriz.loc[nombre_fila]          # selecciona la fila con el nombre asignado( a1,a2,x1,x2,etc )
    return fila
#===========================================================================================================================

# funcion que crea una matriz tipo dataframe de pandas
def crear_matriz():
    restricciones = ampliar_restricciones()
    variables = obtener_variables(restricciones)
    
    var_artificiales = seleccionar_variables_artificiales(variables,'a')    # se obtiene una lista de las variables artificiales
   
    # se crea la funcion Z con las variables artificiales
    cadena_valores = ' + '.join(var_artificiales)                           # Crear la cadena de caracteres usando la función join()
    z = f'Z + {cadena_valores} = 0'                                         # Crear la cadena final usando un f-string
    restricciones.insert(0,z)                                               #se agrega la funcion z a la lista de restricciones

    coeficientes = obtener_coeficientes(restricciones,variables)            # se obtienen la lista de valores numericos

    # formar los nombres para las filas      
    holguras = seleccionar_variables_artificiales(variables,'h')            # se obtiene una lista de las variables de holgura
    filas = var_artificiales + holguras                                     # se juntan las listas 
    filas.insert(0,'Z')                                                     # se agrega la variable Z al inicio de la lista

    print(restricciones)
    print(variables)

    # crear dataframe con los datos
    matriz = pd.DataFrame(coeficientes, columns=variables, index=filas)
    print(matriz)
    return matriz

#===========================================================================================================================
#restricciones = 60x1 + 60x2 >= 300, 12x1 + 6x2 >= 36,10x1 + 30x2 >= 90,x1 >= 0, x2 >= 0

# restricciones = xeA + xoA >= 40, xeB + xoB >= 70, 2xeA + 2xoA <= xeB + xoB, xeA + xeB <= 180, xoA + xoB <= 45, xij >= 0
# restricciones = xeA + xoA >= 40, xeB + xoB >= 70, xeA + xeB <= 180, xoA + xoB <= 45, xij >= 0
# restricciones = x1 + x2 >= 40, x3 + x4 >= 70,2x1 + 2x2 - x3 - x4 <= 0, x1 + x3 <= 180, x2 + x4 <= 45, x5 >= 0
#variables = ['Z', 'e1', 'a1', 'x1', 'e2', 'a2', 'x2', 'e3', 'a3', 'LD']

#===========================================================================================================================

# funcion que calcula la columna pivote ( recibe la matriz y el nombre de la columna que se quiere tratar) 
def obtener_fila_pivote(matriz,columna):
    LD = matriz.iloc[:, -1]                         # seleccionar columna del lado derecho                           
    col = seleccionar_columna(matriz,columna)       # obtiene una columna entera del dataframe(matriz)
    # ciclo para dividir el lado derecho por la columna pivote 
    indice_minimo = float(0)
    division_previa = 100000000000000000000000
    for i in range(len(LD)):
        if(col[i]>float(0) and LD[i]>float(0)):    # evitar divisones por 0 y negativos
            division = float(LD[i] / col[i])
            if division < division_previa:
                division_previa = division
                indice_minimo = i
    return indice_minimo
       
#===========================================================================================================================

# funcion que hace reduccion gaussiana y retorna una matriz con los nuevos valores (recibe una matriz y el nombre de la columna)
def reduccion_gauss(matriz,columna):
    # guardar datos de la matriz actual para luego crear la nueva
    variables = matriz.columns
    index = matriz.index

    getcontext().prec = 4           # se limitan los decimales

    columna_pivote = seleccionar_columna(matriz, columna)       # selecciona la columna pivote
    num_fila_pivote = obtener_fila_pivote(matriz, columna)      # obtiene la posicion de la fila pivote
    fila_pivote = seleccionar_fila(matriz,num_fila_pivote)      # selecciona la fila pivote
    pivote = matriz.loc[fila_pivote.name,columna_pivote.name]   # obtiene el valor del pivote

    # divide la fila pivote por el valor del pivote
    for i in range(len(fila_pivote)):
        fila_pivote[i] = fila_pivote[i]/pivote
    #print(fila_pivote)
    matriz_aux = []
    col_piv = list(columna_pivote)              # se guardan los valores de la columna pivote antes de los cambios
    
    # para cada fila restante: valor_actual - (valor_columna_pivote * valor_fila_pivote)
    for i in range(len(columna_pivote)):
        if i!=num_fila_pivote:                  # solo si NO es la fila pivote
            fila_aux = seleccionar_fila(matriz,i)

            # ciclo que hace la operacion
            for j in range(len(fila_aux)):
                mult = Decimal(col_piv[i])*Decimal(fila_pivote[j])          # se utiliza Decimal para limitar la cantidad de decimales a operar
                fila_aux[j] = Decimal(fila_aux[j])-Decimal(mult)

            matriz_aux.insert(i,fila_aux)       # se inserta el valor obtenido en la posicion indicada

            fila_aux = []     # vaciar la fila auxiliar.
        # en caso de ser la fila pivote, guardar la fila directamente en la matriz auxiliar
        else:                               
            fila_aux = seleccionar_fila(matriz,i)
            matriz_aux.insert(i,fila_aux)
            fila_aux = []     # vaciar la fila auxiliar
    
    # crear nueva matriz con los nuevos datos
    nueva_matriz = pd.DataFrame(matriz_aux, columns=variables, index=index)

    nueva_matriz = nueva_matriz.applymap(convertir_cero)
    print(nueva_matriz)
    return nueva_matriz
#===========================================================================================================================

# funcion especial que se utiliza para convertir los ceros en notacion cientifica de la matriz en ceros, ( se aplica a la matriz mediante applymap tal que : matriz.applymap(convertir_cero) )
def convertir_cero(x):
    if isinstance(x, Decimal) and "E+" in str(x):       #verifica si existe notacion cientifica en el valor
        if x.is_zero():                                 # si el valor es cero
            return Decimal(0)                           # retornar el numero convertido a 0 decimal
    return x                                            # en caso contrario retornar el mismo valor previo

# funcion que busca el valor minimo de una fila ( recibe una matriz y la posicion de la fila)
def buscar_columna_pivote(matriz, pos_fila):
    fila_z = seleccionar_fila(matriz, pos_fila)     # seleccionar la fila Z
    fila_z.pop('LD')                                # eliminar la columna LD
    fila_z.pop('Z')                                 # eliminar columna Z, para evitar que se detecte un negativo en caso de minimizacion
    minimo = min(fila_z)                            # buscar el valor minimo dentro de la fila

    indice_minimo = fila_z.astype(float).idxmin()   # buscar el indice del valor minimo ( se convierte la fila en float para que el metodo idxmin() reconozca los datos)

    if minimo < 0 :                                 # si el valor minimo es negativo
        return [indice_minimo,True]                 # retornar el indice (nombre de la columna)  y una flag True         
    else:                                           
        return [indice_minimo,False]                # si es positivo retornar flag = False
                      
#===========================================================================================================================
def ampliar_funcion_z(fz):
    # entrada :  z = '-Z + 0.12x1 + 0.15x2 = 0'
    # salida  :  z = [-1,0.12,0.0,0.15,0.0,0.0,0]

    
    funcion_z = 0
    return funcion_z


# funcion que crea la matriz de la fase 2, ( recibe la matriz y la funcion Z ampliada en forma de lista ordenada segun las variables)
def crear_2da_matriz(matriz, z_ampliado):
    var_artificiales = seleccionar_variables_por_nombre(matriz,'a')
    matriz = matriz.drop(columns = var_artificiales)
    matriz.loc['Z'] = z_ampliado
    
    print(matriz)
    return matriz

if __name__ == "__main__":
#===========================================================================================================================
#################### Zona de testeo ########################################################################################
#===========================================================================================================================
    matriz = crear_matriz()     # crear matriz con los datos

    columnas_artificiales = seleccionar_variables_por_nombre(matriz,'a')    #seleccionar la lista de columnas a trabajar

    for i in range(len(columnas_artificiales)):
        matriz = reduccion_gauss(matriz,columnas_artificiales[i])    # se actualiza la matriz con la nueva matriz constantemente

    #restricciones = 60x1 + 60x2 >= 300, 12x1 + 6x2 >= 36,10x1 + 30x2 >= 90

    negativo = True
    while negativo == True:
        columna_pivote = buscar_columna_pivote(matriz,0)            # buscar columna pivote en la fila Z
        negativo = columna_pivote[1]                                # verfica si la columna pivote tiene un valor negativo
        if negativo == True:                                        # si es negativo se hace la reduccion
            matriz = reduccion_gauss(matriz,columna_pivote[0])      # reduccion gaussiana


#z = '-Z + 0.12x1 + 0.15x2 = 0'
#z = [-1,0.12,0,0.15,0,0,0]
#crear_2da_matriz(matriz, z)
