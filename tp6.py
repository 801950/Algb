# ---------------------------------------------------------------------------
# File: tp6.py
# Date: Junio 2022
# Author: Nerea Gallego Sanchez
# ---------------------------------------------------------------------------
# Resuelve el problema de la mudanza planteado en el trabajo tp6 de la 
# Asignatura de Algoritmia Básica en la Universidad de Zaragoza
# ---------------------------------------------------------------------------
from multiprocessing.dummy import Array
from telnetlib import BINARY
from itertools import product
from sys import stdout as out
from mip import Model, xsum, maximize, BINARY
from sys import stdin as input
import sys
import numpy as np
from inputdata import read_dat_file

if len(sys.argv) == 2:
    # se leen los datos de entrada
    x, y, c, P, V = read_dat_file(sys.argv[1])
    if len(x) != len(y):
        out.write('el vector de pesos de los objetos y el vector de volumenes de los objetos deben tener el mismo tamaño')
        exit(1)
    if len(c) != len(P):
        out.write('el vector de coste de las cajas y el vector de peso de las cajas deben tener el mismo tamaño')
    if len(c) != len(V):
        out.write('el vector de coste de las cajas y el vector de volumenes de las cajas deben tener el mismo tamaño')
else:
    out.write('Uso: python3 %s <namefile>.dat' % sys.argv[0])
    exit(1)

nbObjetos, nbCajas = len(x), len(c)

# se crea el modelo del problema
m = Model("Mudanza")

w = [[ m.add_var(var_type=BINARY) for j in range(nbCajas)] for i in range(nbObjetos)] # el objeto i está en la caja j
z = [m.add_var(var_type=BINARY) for j in range(nbCajas)] # hay algún objeto en la caja

# función objetivo: minimizar el coste
m.objective = maximize(-xsum(c[j]*z[j] for j in range(nbCajas)))

# restricción: cada objeto solo puede estar en una caja

for i in range(nbObjetos):
    m += xsum(w[i][j] for j in range(nbCajas)) == 1

# restricción: la cantidad de peso que tiene una caja es menor que la cantidad de peso que soporta

for j in range(nbCajas):
    m += xsum(x[i]*w[i][j] for i in range(nbObjetos)) <= P[j] * z[j]

# restricción: la cantidad de volumen que puede contener una caja es menor que la cantidad de volumen máxima de una caja

for j in range(nbCajas):
    m += xsum(y[i]*w[i][j] for i in range(nbObjetos)) <= V[j] * z[j]

# restricción: si hay algún objeto en la caja, la caja está ocupada

for j in range(nbCajas):
    for i in range(nbObjetos):
        m += w[i][j] <= z[j]

m.optimize()

out.write('Cantidad de objetos %g, cantidad de cajas %g\n' % (nbObjetos, nbCajas))

if m.num_solutions:
    out.write('distribution found with cost %g\n'
              % (-m.objective_value))
    for j in range(nbCajas):
        out.write('Caja %g' % (j+1))
        for i in range(nbObjetos):
            if w[i][j].x >= 0.99:
                out.write(' objeto %g' % (i+1))
        out.write('\n')