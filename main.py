from simplex import getDesigualdad, simplex_m2f, simplex_estandar, patron as coeficiente
import pandas as pd
import re

r = input("Ingrese sus restricciones separando cada una con una coma: ")
res = r.split(",")

Z = input("Ingrese la función objetivo: ")

symbol = re.compile("[a-zA-Z]\d{0,}") #Validar variables
digit = re.compile("(^\W[0-9]{1,})|(^[0-9]{1,})|(^\-{1}\W{0,}[0-9]{1,})") #Validar digitos
ld = re.compile("={1}\W{0,}\d{1,}") # Validar lado derecho

#search = coeficiente.finditer(Z)
#print(list(search))

des = getDesigualdad(res)

# Primer caso: encontrar más de 2 desigualdades
if len(des) > 1:
    simplex_m2f
else:
    # Segundo caso: encontrar una desigualdad
    if des[0] == "<=":
        columns = []
        coe = []
        # Ampliar la función objetivo
        z = list(coeficiente.finditer(Z))

        template = ""
        for e in range(1, len(z)):
            template += "- {} ".format(z[e].group())

        z_ampliado = z[0].group() + template + "= 0"
        z_ampliado = re.sub("\s", "", z_ampliado)
        print("====================Función objetivo ampliado====================")
        print(z_ampliado)
        c_z_ampliado = list(coeficiente.finditer(z_ampliado))

        coef_z = {}
        
        for column in c_z_ampliado:
            coeficiente_z = column.group()
            #print(coeficiente_z)
            sym_z = symbol.search(coeficiente_z)
            if sym_z.group() not in columns:
                columns.append(sym_z.group())
            d = digit.search(coeficiente_z)
            #print(d)
            if d == None:
                coef_z[sym_z.group()] = 1
            else:
                coef_z[sym_z.group()] = d.group()
        coe.append(coef_z)

        # Ampliar restricciones (con holguras)
        restricciones_ampliadas = []
        for r in range(len(res)):
            split = res[r].split(des[0])
            holgura = "h{}".format(r+1)
            restriccion_ampliada = "{}+ {} ={}".format(split[0],holgura,split[1])
            restricciones_ampliadas.append(restriccion_ampliada)
        print("====================Restricciones Ampliadas====================")
        print(restricciones_ampliadas)

        for f in restricciones_ampliadas:
            c = coeficiente.finditer(f)
            s = list(c)
            
            coefis = {}
            for i in s:
                # Buscar variables de holgura y agregarlas a la columna del dataframe
                sym = symbol.search(i.group())
                if sym.group() not in columns:
                    columns.append(sym.group())
                # Buscar coeficientes
                search = digit.search(i.group())
                if search == None:
                    coefis[sym.group()] = 1
                else:
                    coefis[sym.group()] = search.group()
            # Determinar el lado derecho y agregarlo.
            lado_derecho = ld.search(f)
            l_d = digit.search(lado_derecho.group()[1:])
            coefis["LD"] = l_d.group()
            coe.append(coefis)
        columns.append("LD")
            
        # Armar la matriz
        df = pd.DataFrame(data = coe, columns=columns)

        # Limpiar valores NaN del dataframe
        for i in range(len(df)):
            df.loc[i] = df.loc[i].fillna(0)

        # Exportar dataframe
        df.to_csv("./data1.csv")

        print("====================Dataframe====================")
        print(df)
        print("====================Array de Numpy====================")
        arr = df.to_numpy()
        print(arr)

        print("====================Método====================")
        simplex_estandar()
    else:
        simplex_m2f()