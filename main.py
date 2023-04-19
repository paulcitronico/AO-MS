from simplex import getDesigualdad, simplex_m2f, simplex_estandar

Z = "-2x1 - 2x2"

res = [
    "2x1 + x2 >= 100",
    "x1 + 3x2 >= 80",
    "x1 >= 45",
    "x2 >= 100"
]

des = getDesigualdad(res)

# Primer caso: encontrar más de 2 desigualdades
if len(des) > 1:
    simplex_m2f
else:
    # Segundo caso: encontrar una desigualdad
    if des[0] == ">=":
        simplex_estandar()
    else:
        simplex_m2f()