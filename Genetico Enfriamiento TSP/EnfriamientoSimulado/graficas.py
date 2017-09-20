import matplotlib.pyplot as plt
import numpy as np
import sys

# --------------------------------------------------------------------------------------
# Prrograma para obtener graficas
# --------------------------------------------------------------------------------------
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TIA
# Lenguaje: python2.7
# --------------------------------------------------------------------------------------

# Comprobacion de parametros de entrada
if len(sys.argv) != 2:
	print "----------------------------------------------------------------------------"
	print "Uso: python2.7 graficas.py <tabla_obtenida>"
	print "----------------------------------------------------------------------------"
	print "<tabla_obtenida>: Tabla obtenida por el programa python2.7 'obtener_tablas.py'"
	sys.exit(0)

# Almacenamos parametros
fichero = sys.argv[1]

f_entrada = open(fichero,'r')
tabla = f_entrada.read()

x = [100,1000,10000,30000] # Iteraciones
cf = ['g-d','r-d','b-d','y-d']

# Obtenemos las filas de la tabla
filas_tabla = tabla.split("\n")[0:len(tabla.split("\n"))-1]


max_y = float('-Inf')
min_y = float('Inf')
for i in range(len(filas_tabla)):
	y = filas_tabla[i].split("\t")[0:len(filas_tabla[i].split("\t"))-1]
	for j in range(len(y)):
		y[j] = int(round(float(y[j].strip()),4))
		if y[j] > max_y:
			max_y = y[j]
		elif y[j] < min_y:
			min_y = y[j]
	plt.plot(x,y,cf[i])
plt.legend(['ind_poblacion = 5','ind_poblacion = 10','ind_poblacion = 20','ind_poblacion = 30'])
plt.xlim(-5000,35000)
plt.ylim(int(min_y)-int(min_y)/5,int(max_y)+int(max_y)/5)
plt.xlabel('Numero de Generaciones')
plt.ylabel('Solucion: Distancia del recorrido')
plt.show()




