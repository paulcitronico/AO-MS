import re
import pandas as pd
import numpy as np
from decimal import Decimal, getcontext

#restricciones = 60x1 + 60x2 >= 300, 12x1 + 6x2 >= 36,10x1 + 30x2 >= 90

# funcion que amplia las restricciones segun sea el caso 
def ampliar_restricciones(restricciones):
    
    restricciones_ampliadas = []                                    # lista para guardar las restricciones ampliadas
    patron = r'[<=>]='                                              # patron que detecta los operadores <=,>=,=
    restricciones = [r.strip() for r in restricciones.split(",")]   # separa la lista de restricciones basandose en la coma(,)
    
    for i, restriccion in enumerate(restricciones):
        operador = re.findall(patron, restriccion)                  # obtiene el operador de cada restriccion ( >=,<= )

        # En caso de que no encuentre ningun operador se termina el proceso
        if len(operador) == 0:
            print(f"No se encontró operador en la restricción {restriccion}")
            break
            
        #se separa la restriccion 
        res_izq, res_der = restriccion.split(operador[0])           # separa la restriccion en base al operador ( separa el lado derecho del resto )
        res_der = int(res_der.strip())                              # Lado derecho de la restriccion
        
        # si es menor o igual : crear variables de holgura entre el lado izquierdo y lado derecho asignando como operador "="
        if "<=" in restriccion:                      
            var_holgura = f"h{i+1}"             # variable de holgura, comienza con la letra "h" seguida de numeros
            restriccion_ampliada = f"{res_izq} + {var_holgura} = {res_der}"

        # si es mayor o igual : restar variable de exceso y sumar variable artificial entre el lado izquierdo y derecho de la restriccion 
        elif ">=" in restriccion:
            var_exceso = f"e{i+1}"              # variable de exceso, comienza con la letra "e" seguida de numeros
            var_artificial = f"a{i+1}"          # variable artificial, comienza con la letra "a" seguida de numeros
            restriccion_ampliada = f"{res_izq} - {var_exceso} + {var_artificial} = {res_der}"
        
        #agregar a la lista de restricciones ampliadas
        restricciones_ampliadas.append(restriccion_ampliada)

    return restricciones_ampliadas

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
                
    #ordenar las variables ( se ordenan segun los numeros de la variable ej: a1,e1,x1,a2,e2,x2,etc...)
    variables.sort(key=lambda x: x[1:] if len(x) > 1 else x)
    
    return variables
   
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

        #en caso de la restriccion para ampliar la funcion Z
        func_z = restriccion.split('=')[0].strip()
        if func_z == 'Z' or func_z == 'z':
            return tuplas_coeficientes
        else:
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

            LD = restriccion.split('=')[1].strip()                  # se separa y obtiene el lado derecho de la restriccion
            
            constante = float(LD)                                               # se separa la constante por el simbolo =
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

# funcion que crea una matriz tipo dataframe de pandas( recibe un string de restricciones separadas por comas, tambien recibe una flag True o False para saber si el problema es de minimizacion)
def crear_matriz(res,minimizacion):
    restricciones = ampliar_restricciones(res)
    variables = obtener_variables(restricciones)

    #agregar Z y LD en sus posiciones
    variables.insert(0, "Z")
    variables.append("LD")

    var_artificiales = seleccionar_variables_artificiales(variables,'a')    # se obtiene una lista de las variables artificiales
   
    # se crea la funcion Z con las variables artificiales
    cadena_valores = ' + '.join(var_artificiales)                           # Crear la cadena de caracteres usando la función join()
    if minimizacion == True:
        z = f'-Z + {cadena_valores} = 0'
    else:
        z = f'Z + {cadena_valores} = 0'                                     # se crear la cadena final usando un f-string
    restricciones.insert(0,z)                                               # se agrega la funcion z a la lista de restricciones

    coeficientes = obtener_coeficientes(restricciones,variables)            # se obtienen la lista de valores numericos

    # formar los nombres para las filas      
    holguras = seleccionar_variables_artificiales(variables,'h')            # se obtiene una lista de las variables de holgura
    filas = var_artificiales + holguras                                     # se juntan las listas 
    filas.insert(0,'Z')                                                     # se agrega la variable Z al inicio de la lista

    # crear dataframe con los datos
    matriz = pd.DataFrame(coeficientes, columns=variables, index=filas)
    print(matriz)
    return matriz

#===========================================================================================================================

# funcion que calcula la columna pivote ( recibe la matriz y el nombre de la columna que se quiere tratar) 
def obtener_fila_pivote(matriz,columna):
    LD = matriz.iloc[:, -1]                         # seleccionar columna del lado derecho                           
    col = seleccionar_columna(matriz,columna)       # obtiene una columna entera del dataframe(matriz)
    # ciclo para dividir el lado derecho por la columna pivote 
    indice_minimo = float(0)
    division_previa = 100000000000000000000000      # se crea un numero muy grande para la primera comparacion en la division
    for i in range(len(LD)):
        if(col[i]>float(0) and LD[i]>float(0)):     # evitar divisones por 0 y negativos
            division = float(LD[i] / col[i])
            if division < division_previa:          # en caso de que el valor actual sea menor que el anterior
                division_previa = division          # guarda el valor mas bajo
                indice_minimo = i                   # guarda el indice del valor mas bajo
    return indice_minimo
       
#===========================================================================================================================

# funcion que hace reduccion gaussiana y retorna una matriz con los nuevos valores (recibe una matriz y el nombre de la columna)
def reduccion_gauss(matriz,columna):
    # guardar datos de la matriz actual para luego crear la nueva
    variables = matriz.columns
    index = matriz.index

    getcontext().prec = 6           # se limitan los decimales para las operaciones

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

            matriz_aux.insert(i,fila_aux)       # se inserta la fila obtenida en la posicion indicada

            fila_aux = []     # vaciar la fila auxiliar.
        # en caso de ser la fila pivote, guardar la fila directamente en la matriz auxiliar
        else:                               
            fila_aux = seleccionar_fila(matriz,i)
            matriz_aux.insert(i,fila_aux)
            fila_aux = []     # vaciar la fila auxiliar
    
    # crear nueva matriz con los nuevos datos
    nueva_matriz = pd.DataFrame(matriz_aux, columns=variables, index=index)

    nueva_matriz = nueva_matriz.applymap(convertir_cero)        # convierte los ceros en notacion cientifica de la matriz a ceros en Decimal

    print(nueva_matriz)
    return nueva_matriz
#===========================================================================================================================

# funcion especial que se utiliza para convertir los ceros en notacion cientifica de la matriz en ceros, ( se aplica a la matriz mediante applymap tal que : matriz.applymap(convertir_cero) )
def convertir_cero(x):
    if isinstance(x, Decimal) and "E+" in str(x) or "E-" in str(x) :       #verifica si existe notacion cientifica en el valor
        if x.is_zero():                                 # si el valor es cero
            return Decimal(0)                           # retornar el numero convertido a 0 decimal
    return x                                            # en caso contrario retornar el mismo valor previo

#===========================================================================================================================

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
def ampliar_funcion_z(matriz,fz):
    z_list = []
    arr_z = []
    z_list.append(fz)       # se ingresa la funcion z en una lista para su correcto funcionamiento en los metodos a utilizar
    variables_z = []
    coeficientes_z = []

    tuplas_datos = obtener_coeficientes(z_list,variables_z)     #se obtiene una serie de tuplas con las variables y coeficientes separados de la funcion z

    for tupla in tuplas_datos:
        coeficientes_z.append(tupla[0])     # se guardan los coeficientes
        variables_z.append(tupla[1])        # se guardan las variables

    for i in range(len(coeficientes_z)):
        if coeficientes_z[i] == '':         #si Z no tiene ningun numero antes 
            if minimizacion == True:        # si es un problema de minimizacion
                coeficientes_z[i] = -1      # indicar que Z vale -1
            else:
                coeficientes_z[i] = 1       # si es problema de maximizacion indicar que z vale 1
        
    variables_matriz= list(matriz.columns)  # lista de variables

    # verifica si la variable de z se encuentra en la lista de la matriz
    for var_mat in variables_matriz:
        if var_mat in variables_z:          
            i = variables_z.index(var_mat)          # se obtiene el indice(nombre) de la variable
            arr_z.append(float(coeficientes_z[i]))  # se agrega a la lista arr_z el coeficiente de z
        else:
            arr_z.append(0)                         # si no existe en la lista se agrega un 0 en la posicion
    return arr_z

#===========================================================================================================================

# funcion que crea la matriz de la fase 2, ( recibe la matriz y la funcion Z ampliada en forma de lista ordenada segun las variables)
def crear_2da_matriz(matriz, z_ampliado):
    var_artificiales = seleccionar_variables_por_nombre(matriz,'a')     # se buscan las variables que comienzan con a (variables artificiales)
    matriz.loc['Z'] = z_ampliado                                        # se selecciona la fila Z de la matriz
    matriz = matriz.drop(columns = var_artificiales)                    # se borran las columnas artificiales
    
    print(matriz)
    return matriz

#===========================================================================================================================
#################### Zona de testeo ########################################################################################
#===========================================================================================================================
res = input("Introducir las restricciones separadas por coma: ")
fz = input("Introducir la funcion Z: ")
minimizacion = input("¿ Es un problema de minimización ? : Si / No")
# guarda el valor booleano que indica si es un problema de minimizacion
if minimizacion == "si" or minimizacion == "SI" or minimizacion == "Si" or minimizacion == "s" or minimizacion == "S":
    minimizacion = True
else:
    minimizacion = False

def m2f_main(res,fz,minimizacion):
    #===========================================================================================================================
    #################### Fase 1 ################################################################################################
    #===========================================================================================================================
    # crear matriz con los datos ( recibe las restricciones y una flag indicando si es un problema de minimizacion)
    matriz_fase_1 = crear_matriz(res,minimizacion)    

    columnas_artificiales = seleccionar_variables_por_nombre(matriz_fase_1,'a')     # seleccionar la lista de columnas artificiales

    # reduccion gaussiana a las variables artificiales
    for i in range(len(columnas_artificiales)):
        matriz_fase_1 = reduccion_gauss(matriz_fase_1,columnas_artificiales[i])     # se actualiza la matriz con la nueva matriz constantemente

    columnas_negativas = buscar_columna_pivote(matriz_fase_1,0)
    columnas = seleccionar_variables_por_nombre(matriz_fase_1,'x')      # seleccionar la lista de columnas a trabajar

    for i in range(len(columnas)):
        matriz_fase_1 = reduccion_gauss(matriz_fase_1,columnas[i])

    # ciclo de reduccion gaussiana para el resto de variables
    count = 0                                                                      # contador para limitar el numero de iteraciones ( en caso de que el problema no tenga solucion o se escribiera mal)
    negativo = True
    while negativo == True or count > 50:
        count = count + 1
        columna_pivote = buscar_columna_pivote(matriz_fase_1,0)                    # buscar columna pivote en la fila Z
        negativo = columna_pivote[1]                                               # verfica si la columna pivote tiene un valor negativo
        if negativo == True:                                                       # si es negativo se hace la reduccion
            matriz_fase_1 = reduccion_gauss(matriz_fase_1,columna_pivote[0])       # reduccion gaussiana

            pos_fila = obtener_fila_pivote(matriz_fase_1,columna_pivote[0])                     # obtiene el numero de la fila
            fila_pivote = seleccionar_fila(matriz_fase_1,pos_fila)                              # obtiene la fila pivote
            matriz_fase_1 = matriz_fase_1.rename(index={fila_pivote.name:columna_pivote[0]})    # cambia el nombre de la fila pivote por el nombre de la columna pivote con la que acaba de hacer reduccion gaussiana
    #===========================================================================================================================
    #################### Fase 2 ################################################################################################
    #===========================================================================================================================

    z_ampliado = ampliar_funcion_z(matriz_fase_1,fz)                    # transforma la funcion Z en un arreglo de numeros del tamaño adecuado para la matriz
    matriz_fase_2 = crear_2da_matriz(matriz_fase_1, z_ampliado)         # crea la 2da matriz en base a la primera eliminando las columnas artificiales y reemplazando la fila z con los valores de la funcion Z

    columnas = seleccionar_variables_por_nombre(matriz_fase_2,'x')      # seleccionar la lista de variables basicas que comienczan con 'x'
    columnas_negativas = buscar_columna_pivote(matriz_fase_2,0)         # busca el valor minimo y guarda su valor y si es negativo ([valor,True])

    # en caso de que todos los valores de las variables basicas sean positivas, hacer reduccion gaussiana en orden a cada una de ellas
    if bool(columnas_negativas[1]) == False: 
        for i in range(len(columnas)):
            matriz_fase_2 = reduccion_gauss(matriz_fase_2,columnas[i])  # se actualiza la matriz con la nueva matriz constantemente

    # revisar si hay negativos nuevamente, para evitar reducciones innesesarias
    columnas_negativas = buscar_columna_pivote(matriz_fase_2,0)         # busca el valor minimo y guarda su valor y si es negativo ([valor,True])

    #ciclo de reduccion gaussiana para la segunda fase
    count = 0                                                           # contador para limitar el numero de iteraciones ( en caso de que el problema no tenga solucion o se escribiera mal)
    negativo = bool(columnas_negativas[1])                              # booleano que guarda si el valor minimo de la fila Z es negativo
    while negativo == True or count > 50:
        count = count + 1
        columna_pivote = buscar_columna_pivote(matriz_fase_2,0)                    # buscar columna pivote en la fila Z
        negativo = columna_pivote[1]                                               # verfica si la columna pivote tiene un valor negativo  
        if negativo == True:                                                       # si es negativo se hace la reduccion
            matriz_fase_2 = reduccion_gauss(matriz_fase_2,columna_pivote[0])       # reduccion gaussiana

            pos_fila = obtener_fila_pivote(matriz_fase_2,columna_pivote[0])                     # obtiene el numero de la fila
            fila_pivote = seleccionar_fila(matriz_fase_2,pos_fila)                              # obtiene la fila pivote
            matriz_fase_2 = matriz_fase_2.rename(index={fila_pivote.name:columna_pivote[0]})    # cambia el nombre de la fila pivote por el nombre de la columna pivote con la que acaba de hacer reduccion gaussiana
