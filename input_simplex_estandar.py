# Módulo con métodos relacionados a la entrada de datos
import re
import pandas as pd

terminos = re.compile("(\-{0,1}\s{0,}\d{0,}[a-zA-Z]{1}\d{1})|[zZ]") # Validar términos, ejemplo X1, 3x2, -4x1, etc.
symbol = re.compile("[a-zA-Z]\d{0,}") #Validar variables
digit = re.compile("(^\W[0-9]{1,})|(^[0-9]{1,})|(^\-{1}\W{0,}[0-9]{1,})") #Validar digitos
ld = re.compile("={1}\W{0,}\d{1,}") # Validar lado derecho

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