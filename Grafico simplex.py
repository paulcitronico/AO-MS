import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog
import sympy
from matplotlib.path import Path
from matplotlib.patches import PathPatch

#FALTA CAMBIAR LO DE LAS RESTRICCIONES Y ALGUNA QUE OTRA OPCION QUE PUEDA SURGIR

def vRestric():

    masdata = input('¿Tiene valores? (si/no) ')
    valoresxy = np.empty((0, 2), int) #los (0,2) indica la dimension del array, lo mismo para los 2
    LDrest = np.empty((0, 1), int)

    while masdata.lower() == 'si': #ciclo para ingresar los valores de los multiplicadores de x y el lado derecho de las restricciones
        print('Ingrese los multiplicadores para cada x y el lado derecho para cada recta')

        x1 = int(input('Valor para x1: '))
        x2 = int(input('Valor para x2: '))
        ld = int(input('Valor para ld: '))



        valoresxy = np.append(valoresxy, np.array([[x1, x2]]), axis=0)
        LDrest = np.append(LDrest, np.array([[ld]]), axis=0)

        masdata = input('¿Tiene más valores? (si/no) ')

    print("valoresxy:\n", valoresxy) #verifica la data de los array
    print("LDrest:\n", LDrest)

    x1_ = (0, None)
    x2_ = (0, None)

    ecuaciones = []
    num_ecuaciones = int(input("Ingrese la cantidad de ecuaciones: "))
    for i in range(num_ecuaciones):
        ecuacion = input(f"Ingrese la ecuación {i + 1}: ")
        ecuaciones.append(ecuacion)
    print(ecuaciones)

    x = sympy.symbols('x')
    #fig, ax = plt.subplots(figsize=(8, 8))
    x_vals = np.linspace(0, 60, 10000)
    for ecuacion in ecuaciones:
        try:
            f = sympy.sympify(ecuacion)
            y_vals = np.array([f.subs(x, i) for i in x_vals])
            plt.plot(x_vals, y_vals, label=ecuacion)
            # plt.fill_between(x_vals, y_vals, alpha=0.1)
        except:
            print(f"La ecuación {ecuacion} no es válida")

    #PARAMETROS VARIOS DEL GRAFICO EN GENERAL
    plt.axhline(0, color="black")
    plt.axvline(0, color="black")
    plt.xlim(x1_)
    plt.ylim(x2_)
    plt.xlabel("x")
    plt.ylabel('y')
    plt.legend()

    c = np.array([-22, -45])
    res = linprog(c, A_ub=valoresxy, b_ub=LDrest, bounds=(x1_, x2_), method='highs') #con los datos ingresados se calcula el punto maximo
    vert = (res.x[0], res.x[1])
    plt.plot(vert[0], vert[1], 'ro', markersize=10)
    plt.show()

vRestric()
