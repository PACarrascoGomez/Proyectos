import sys, os
import random
import math

####################################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Algoritmo k vecinos mas cercanos
# Corpus: Flores: Virginica, Setosa, Versicolor (150 muestas etiquetadas)
# Entorno: python3
####################################################################

# Ejemplo ejecucion: python3 kneighbours.py iris.dat 1

#-------------------------------------------------------------------
# FUNCIONES
#-------------------------------------------------------------------
def d_euclidea(x,y):
	suma = 0.0
	for i in range(len(x)):
		suma += (x[i]-y[i])*(x[i]-y[i])
	return math.sqrt(suma)

#-------------------------------------------------------------------
# PARAMETROS
#-------------------------------------------------------------------
# Comprobacion de parametros de entrada
if len(sys.argv) != 3:
	print ("Uso: python3 kneighbours.py <data.dat> <k>")
	exit()

# Asignacion de parametros
dat = sys.argv[1]
k = int(sys.argv[2])

#-------------------------------------------------------------------
# PREPROCESO CORPUS (FLORES)
#-------------------------------------------------------------------
# Preproceso de los datos
lineas = os.popen("cat " + dat).read().split("\n")[:-1]
datos = []
for l in lineas:
	aux = l.split(" ")
	for i in range(len(aux)-1):
		aux[i] = float(aux[i])
	datos.append(aux)

# Convertimos las clases en numeros (mayor comodidad y eficiencia)
clases = []
for d in datos:
	if d[4] not in clases:
		clases.append(d[4])
dic_clases = {}
dic_inv_clases = {}
for i in range(len(clases)):
	dic_clases[clases[i]] = i
	dic_inv_clases[i] = clases[i]

# Barajamos el corpus (Semilla --> determinismo de ejecucion)
random.seed(5) # Semilla
random.shuffle(datos)

# Particionamos el corpus:
# --> 30 muestras evaluacion (test)
# --> 120 muestras entrenamiento (train)
test = datos[:30]
train = datos[30:]

#-------------------------------------------------------------------
# ALGORITMO K-NEIGHBOURS
#-------------------------------------------------------------------
res_test = [] # Salida para las muestras de test
for y in test:
	distancias = []
	x_y = y[0:4]
	for x in train:
		x_x = x[0:4]
		distancias.append([d_euclidea(x_y,x_x),dic_clases[x[4]]])
	# Ordenamos las distancias de menor a mayor
	distancias.sort(key=lambda z: z[0])
	# Contamos las clases de los k vecinos mas proximos
	cont = len(dic_clases)*[0]
	for i in range(k):
		cont[distancias[i][1]] += 1
	# Obtenemos la clase ganadora
	c = cont.index(max(cont))
	res_test.append(c)

#-------------------------------------------------------------------
# EVALUACION
#-------------------------------------------------------------------
aciertos = 0
for i in range(len(res_test)):
	if dic_clases[test[i][4]] == res_test[i]:
		aciertos += 1
print ("------------------------------------------------")
print ("Resultados:")
print ("------------------------------------------------")
print ("\tAciertos:",aciertos)
print ("\tMuestras analizadas:",len(res_test))
print ("\tMuestras totales:",len(test))
print ("------------------------------------------------")
print ("Medidas de evaluacion:")
print ("------------------------------------------------")
C = len(res_test)/len(test)
P = aciertos/len(res_test)
R = aciertos/len(test)
F1 = (2*P*R)/(P+R)
print ("\tCoverage:",C)
print ("\tPrecision:",P)
print ("\tRecall:",R)
print ("\tF1-score:",F1)



