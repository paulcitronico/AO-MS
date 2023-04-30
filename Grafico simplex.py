import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog
import sympy

def vRestric():
    ################### ENTRADA DE LOS MULTIPLICADORES DE VADA X Y EL LADO DERECHO ###################
    masdata = input('¿Tiene valores? (si/no) ')  # Print para el ingreso de x1, x2 y el lado derecho ld
    valoresxy = np.empty((0, 2), int)  # Arreglo vacio creado con np.empty que tiene una dimension de (0,2), este guarda los valores de x e y en las restricciones
    LDrest = np.empty((0, 1), int) # Arreglo vacio creado con np.empty que tiene una dimension de (0,1), este guarda el lado derecho de las restricciones

    while masdata.lower() == 'si': # While que convierte el string de mas data a minuscula con .lower y si es == 'si' continua
        print('Ingrese los multiplicadores para cada x e y ademas de el lado derecho') # Print para avisarle al usuario lo que debera ingresar

        x1 = int(input('Valor para x1: ')) # Variable que guarda un numero que sera el valor de x1
        x2 = int(input('Valor para x2: ')) # Variable que guarda un numero que sera el valor de x2
        ld = int(input('Valor para ld: ')) # Variable que guarda un numero que sera el valor de lado derecho

        valoresxy = np.append(valoresxy, np.array([[x1, x2]]), axis=0) # se le ingresan las entradas de x1 y x2 al arreglo 'valoresxy' con
        # np.append(arreglo al cual se ingresa los datos, tipo de entrada con el formato del arreglo original
        LDrest = np.append(LDrest, np.array([[ld]]), axis=0) # se le ingresan las entradas de ld al arreglo 'LDrest'

        masdata = input('¿Tiene más valores? (si/no) ') # Se vuelve a preguntar, si la respuesta es si se repite lo anterior de lo contrario se continua

    print("valoresxy:\n", valoresxy) # Print para mostrar los valores ingresados en valoresxy
    print("LDrest:\n", LDrest) # Print para mostrar los valores ingresados en LDrest

    ################### PROCESO DE ENTRADA DE LAS ECUACIONES A GRAFICAR  ###################
    # Las ecuaciones tienen que estar escritas para resolver el valor de y, esto indica que deben tener una x

    x1_ = (0, None) # Tupla para definir un limite que sera desde 0, none; none se puede interpretar como infinito ya que no hay un valor especifico definido
    x2_ = (0, None) # Tupla para definir un limite que sera desde 0, none; none se puede interpretar como infinito ya que no hay un valor especifico definido

    ecuaciones = [] #Arreglo comun de toda la vida que guardara las ecuaciones ingresadas
    num_ecuaciones = int(input("Ingrese la cantidad de ecuaciones: ")) # Variable que recibe una entrada tipo int
    for i in range(num_ecuaciones): # For que recorrera en relacion al numero que reciba la variable anterior
        ecuacion = input(f"Ingrese la ecuación {i + 1}: ") # Variable que recibira la ecuacion mediante un input
        ecuaciones.append(ecuacion) # Al arreglo 'ecuaciones' se le agrega la entrada de ecuacion mediante .append
    print(ecuaciones) # Print para mostrar las ecuaciones ingresadas guardadas en 'ecuaciones'

    ################### INICIO DEL PROCESO GRAFICO ###################

    x = sympy.symbols('x') # Crea un símbolo llamado 'x'. Este símbolo puede ser utilizado para construir expresiones algebraicas
    #fig, ax = plt.subplots(figsize=(8, 8))

    x_vals = np.linspace(0, 60, 1000) # Array unidimencional que servira como limites de graficacion de cada recta, en este caso estan definidas para que partan del 0 a el 60 positivo y genera 1000 valores entre estos
    for ecuacion in ecuaciones: #recorre ecuacion en ecuaciones
        try:
            f = sympy.sympify(ecuacion) # Se utiliza para convertir una cadena de caracteres en una expresión simbólica -> String a ecuacion de sympy
            y_vals = np.array([f.subs(x, i) for i in x_vals]) # En cada iteración, la expresión utiliza el método subs() de SymPy para evaluar la expresión simbólica f en el valor actual de x y esto es iterado en x_vals
            plt.plot(x_vals, y_vals, label=ecuacion) # .plot se usa pra graficar tiene como parametros los valores de x(x_vals), y(y_vals) y el label que ser[a la ecuacion
            # plt.fill_between(x_vals, y_vals, alpha=0.1)
        except:
            print(f"La ecuación {ecuacion} no es válida") #en caso de que la ecuacion no sea valida la rechaza

    ################### PROCESO PARA CALCULAR EL PUNTO MAXIMO ###################

    c = np.array([-22, -45]) # Array NumPy unidimensional que contiene los coeficientes de la función objetivo
    res = linprog(c, A_ub=valoresxy, b_ub=LDrest, bounds=(x1_, x2_), method='highs')
    # A_ub = array NumPy bidimensional que contiene los coeficientes de las restricciones de desigualdad del problema
    # b_ub = array NumPy unidimensional que contiene los límites superiores de las restricciones de desigualdad del problema
    # bounds = tupla que contiene las restricciones de las variables de decisión del problema.
    # contiene el límite inferior y el límite superior de la variable de decisión correspondiente.
    # method = un string que indica el método de solución a utilizar. En este caso, se establece el valor de method en 'highs'
    vert = (res.x[0], res.x[1]) # guarda los valores optimos.
    # res.x[0] y res.x[1] se utiliza para acceder a los valores óptimos de las dos variables de decision.
    # En la sintaxis, res es el objeto OptimizeResult devuelto por la función linprog() y
    # x es un atributo del objeto que contiene los valores óptimos de las variables de decisión
    plt.plot(vert[0], vert[1], 'ro', markersize=10) #se grafica la tupla vert con los valores en su posicion 0 y 1

    ################### PARAMETROS GENERALES PARA EL GRAFICO ###################
    plt.axhline(0, color="black")
    plt.axvline(0, color="black")
    plt.xlim(x1_)
    plt.ylim(x2_)
    plt.xlabel("x")
    plt.ylabel('y')
    plt.legend()


    plt.show()

vRestric()
