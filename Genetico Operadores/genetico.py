import sys
import random

#######################################################################
# Autor: Pascual Andres Carrasco Gomez
# Lenguaje: Python2.7
# Desc: Algoritmo genetico problema operadores matematicos
#######################################################################

def operar(operador,n1,n2):
	if operador == "+": return n1+n2
	elif operador == "-": return n1-n2
	elif operador == "*": return n1*n2
	elif operador == "/": return n1/n2

# Gestion del modo verbose
modo = 0 # 1 = Verbose; 0 = No Verbose
if len(sys.argv) == 2:
	if sys.argv[1] == "-v":
		modo = 1

# Parametros
n = raw_input("Introduce 6 numeros: (ej: 2 5 1 3 5 4)\n")
o = raw_input("Introduce un numero objetivo:\n")
o = float(o)
itei = raw_input("Introduce el numero de iteraciones:\n") # numero de iteraciones inicial
itei = int(itei)
ite = itei # numero de iteraciones
nind = 3 # numero de individuos en la poblacion

ln = n.split(" ") # Convertimos la entrada a lista
if len(ln) != 6: sys.exit("No has introducido 6 numeros.")
ln = map(float,ln) # Convertimos la lista de string a int

# Operaciones con las que trabajamos
op = ["+","-","*","/"]

#------------------------------------------------
# GENERACION DE POBLACION INICIAL
#------------------------------------------------
# Generamos la poblacion inicial de forma aleatoria
lind = [] # Lista de individuos
for i in range(nind):
	laux = []
	for j in range(len(ln)-1):
		z = random.randint(0,len(op)-1)
		laux.append(op[z])
	lind.append(laux)

#------------------------------------------------
# ACTUALIZAMOS PARAMETROS DE CONDICION DE PARADA
#------------------------------------------------
# Obtenemos el valor de las operaciones
lvalores = [] # Lista con los valores de cada individuo de la poblacion
for i in range(len(lind)):
	res = ln[0]
	for j in range(len(lind[i])):
		res = operar(lind[i][j],res,ln[j+1])
	lvalores.append(res)
#------------------------------------------------
# APTITUD
#------------------------------------------------
lapt = lvalores[:] # Copiamos la lista
for i in range(len(lapt)):
	lapt[i] = abs(o-lvalores[i])
# Obtenemos el valor del mejor individuo
valor = lvalores[lapt.index(min(lapt))]

#------------------------------------------------
# VERIFICAR CONDICION DE PARADA
#------------------------------------------------
while ((valor != o) and (ite != 0)):

	if modo == 1: # Modo verbose activado
		print "Iteracion: ",itei-ite
		print "Secuencia de numeros: ",ln
		print "Objetivo: ",o
		print "Poblacion actual: ",lind
		print "Soluciones actuales: ",lvalores
		print "Funcion fitness: ",lapt
	
	#------------------------------------------------
	# SELECCION
	#------------------------------------------------
	# Realizamos la seleccion
	laptaux = lapt[:] # Copiamos la lista en otro objeto
	padres = []
	i_v_min = laptaux.index(min(laptaux)) # indice del valor min en la lista
	padres.append(lind[i_v_min])
	pinf = float("Inf")
	laptaux[i_v_min] = pinf
	i_v_min = laptaux.index(min(laptaux)) # indice del valor min en la lista
	padres.append(lind[i_v_min])

	if modo == 1: # Modo verbose activado
		print "Padres: ",padres

	#------------------------------------------------
	# CRUCE
	#------------------------------------------------
	# Realizamos un cruce uniforme
	hijo1 = []
	hijo2 = []
	lposnore = [] # posiciones de los operadores no repetidos de los padres
	for i in range(len(lind[0])):
		pal = random.randint(1,2) # padre aleatorio 1 o 2
		if pal == 1:
			hijo1.append(padres[0][i])
			hijo2.append(padres[1][i])
		else:
			hijo1.append(padres[1][i])
			hijo2.append(padres[0][i])
		if padres[0][i] != padres[1][i]:
			lposnore.append(i)

	if modo == 1: # Modo verbose activado
		print "Cruce (Uniforme): ", [hijo1,hijo2]

	#------------------------------------------------
	# MUTACION
	#------------------------------------------------
	# Mutacion aleatoria de un gen
	# Hijo 1
	pos = random.randint(0,len(lind[0])-1)
	posop = random.randint(0,len(op)-1)
	hijo1[pos] = op[posop]
	# Hijo 2
	pos = random.randint(0,len(lind[0])-1)
	posop = random.randint(0,len(op)-1)
	hijo2[pos] = op[posop]

	if modo == 1: # Modo verbose activado
		print "Mutaciones: ",[hijo1,hijo2]

	#------------------------------------------------
	# REMPLAZO
	#------------------------------------------------
	laptaux = lapt[:] # Copiamos la lista en otro objeto
	viejos = [] # Valores de los individuos viejos
	iviejos = [] # Indices de los individuos viejos
	i_v_max = laptaux.index(max(laptaux)) # indice del valor max en la lista
	viejos.append(lind[i_v_max])
	iviejos.append(i_v_max)
	minf = float("-Inf")
	laptaux[i_v_max] = minf
	i_v_max = laptaux.index(max(laptaux)) # indice del valor max en la lista
	iviejos.append(i_v_max)
	lind[iviejos[0]] = hijo1
	lind[iviejos[1]] = hijo2

	if modo == 1: # Modo verbose activado
		print "Remplazo (Poblacion actual): ",lind

	#------------------------------------------------
	# ACTUALIZAMOS PARAMETROS DE CONDICION DE PARADA
	#------------------------------------------------
	# Obtenemos el valor de las operaciones
	lvalores = [] # Lista con los valores de cada individuo de la poblacion
	for i in range(len(lind)):
		res = ln[0]
		for j in range(len(lind[i])):
			res = operar(lind[i][j],res,ln[j+1])
		lvalores.append(res)
	#------------------------------------------------
	# APTITUD
	#------------------------------------------------
	lapt = lvalores[:] # Copiamos la lista
	for i in range(len(lapt)):
		lapt[i] = abs(o-lvalores[i])
	# Obtenemos el valor del mejor individuo
	valor = lvalores[lapt.index(min(lapt))]

	# Decrementamos las iteraciones en uno
	ite = ite - 1

	if modo == 1: # Modo verbose activado
		print "############################################################"

# Devolvemos el individuo con mejor aptitud de la poblacion actual
minapt = min(lapt)
individuo = lind[lapt.index(minapt)]
valor = lvalores[lapt.index(minapt)]
print "--------------------------------------------------------------"
print " SOLUCION:"
print "--------------------------------------------------------------"
if modo == 1: # Modo verbose activado
		print "Secuencia de numeros: ",ln
		print "Objetivo: ",o
		print "Poblacion actual: ",lind
		print "Soluciones actuales: ",lvalores
		print "Funcion fitness: ",lapt
print "Individuo: ",individuo
print "Valor: ",valor
print "Iteracion: ",itei-ite
print "--------------------------------------------------------------"