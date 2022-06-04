from telnetlib import BINARY
from mip import Model, MAXIMIZE, CBC, INTEGER, OptimizationStatus
from itertools import product
from sys import stdout as out
from mip import Model, xsum, maximize, BINARY

#m = Model()
m = Model("Mudanza")

x = [0.1, 0.2, 5, 3.8] # peso del objeto
y = [0.3, 0.4, 7, 2.3] # volumen del objeto
c = [0.5,1,3] # coste de la caja
P = [0.1,4,7] # peso máximo para una caja
V = [1,5,7] # volumen máximo para una caja

nbObjetos, nbCajas = len(x), len(c)
out.write('%g objetos, %g cajas\n' % (nbObjetos, nbCajas))

w = [[ m.add_var(var_type=BINARY) for j in range(nbCajas)] for i in range(nbObjetos)] # el objeto i está en la caja j
z = [m.add_var(var_type=BINARY) for j in range(nbCajas)] # hay algún objeto en la caja

# función objetivo: minimizar el coste
m.objective = maximize(-xsum(c[j]*z[j] for j in range(nbCajas)))

# restricción: cada objeto solo puede estar en una caja

for i in range(nbObjetos):
    m += xsum(w[i][j] for j in range(nbCajas)) == 1

# restricción: la cantidad de peso que tiene una caja es menor que la cantidad de peso que soporta

for j in range(nbCajas):
    m += xsum(x[i]*w[i][j] for i in range(nbObjetos)) <= P[j]

# restricción: la cantidad de volumen que puede contener una caja es menor que la cantidad de volumen máxima de una caja

for j in range(nbCajas):
    m += xsum(y[i]*w[i][j] for i in range(nbObjetos)) <= V[j]

# restricción: si hay algún objeto en la caja, la caja está ocupada

for j in range(nbCajas):
    for i in range(nbObjetos):
        m += w[i][j] <= z[j]

m.optimize()

if m.num_solutions:
    out.write('distribution found with cost %g\n'
              % (-m.objective_value))
    for j in range(nbCajas):
        out.write('Caja %g' % (j+1))
        for i in range(nbObjetos):
            if w[i][j].x >= 0.99:
                out.write(' objeto %g' % (i+1))
        out.write('\n')