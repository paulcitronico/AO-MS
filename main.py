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
        dataframes = armar_matriz(Z, res, des[0])        

        #se guarda el df final en una variable
        ultima_tabla_simplex = dataframes[-1].to_numpy()
        # recibimos el nuevo incremento a la restriccion
        incremento_i = str(input("Ingrese el incremento a la restricción: "))
        restriccion_especifica = int(input("Escoga la restricción especifica a aumentar: "))
        #al incremento se le concatena el incremento recibido
        incremento ="+"+incremento_i
        #llamado a la fun 
        resI=resIncrementada(res[restriccion_especifica-1], incremento)
        print(resI)

        resI_2 = res
        template = ""
        d = resI.split("<=")
        exp_mat = re.sub("\s", "", d[1])
        m = exp_mat.split("+")
        c = int(m[0]) + int(m[1])
        template = "{} <= {}".format(d[0],c)
        resI_2[restriccion_especifica-1] = template

        print(resI_2)

        dataframes_2 = armar_matriz(Z=Z, res=resI_2, desigualdad=des[0])

        ultima_tabla_simplex_2 = dataframes_2[-1].to_numpy()

        z_viejo = ultima_tabla_simplex[0][-1]
        z_nuevo = ultima_tabla_simplex_2[0][-1]
        print("Z NUEVO => {}".format(z_nuevo))
        print("Z ANTIGUO => {}".format(z_viejo))
        dif = z_nuevo - z_viejo
        dif_ = dif / int(incremento)
        print(dif)                
        print(dif / int(incremento))
        if dif == dif_:
            print("Cumple")
        else:
            print("No cumple")

    else:
        simplex_m2f()
