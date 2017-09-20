import sys
import math
import random
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------------------
# Algoritmo genetico
# --------------------------------------------------------------------------------------
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TIA
# Problema: Viajante de comercio
# Lenguaje: python2.7
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# PARAMETROS DEL ALGORITMO GENETICO
# --------------------------------------------------------------------------------------
# Comprobacion de parametros de entrada
if len(sys.argv) != 6:
	print "----------------------------------------------------------------------------"
	print "Uso: python2.7 viajante.py <f_tsp> <n_gen> <n_ind_pob> <n_padres> <verbose>"
	print "----------------------------------------------------------------------------"
	print "<f_tsp>: Fichero con las coordenadas del problema TSP (string)"
	print "<n_gen>: Iteraciones = generaciones en el bucle (int)"
	print "<n_ind_pob>: Cantidad de individuos en la poblacion (int)"
	print "<n_padres>: Numero de padres en la seleccion (int)"
	print "<verbose>: Verbose por pantalla (boolean)"
	sys.exit(0)

# Parametros generales para el algoritmo genetico
f_tsp = sys.argv[1]
n_generaciones = int(sys.argv[2])
n_ind = int(sys.argv[3])
n_padres_seleccion = int(sys.argv[4])
modo_verbose = True if sys.argv[5] == "True" else False
mejor_individuo = []
mejor_puntuacion = float("inf")

# Restriccion en el remplazo del algoritmo genetico
if float(n_padres_seleccion) > float(n_ind)/2:
	print "Error: El numero de n_padres_seleccion ha de ser < que n_ind/2"
	sys.exit(0)

# --------------------------------------------------------------------------------------
# GENERACION DE EDAs PARA EL ALGORITMO GENETICO
# --------------------------------------------------------------------------------------
# Fichero con coordenadas del mapa
nombre_f = f_tsp

# Abrimos el fichero para trabajar con el
fichero = open(nombre_f, 'r')

# Insertamos los datos del fichero en una lista para trabajar con ella
# dato[0] = nodo; dato[1] = x; dato[2] = y;
datos = [] 
for linea in fichero:
	datos_linea = linea.split()
	datos.append(datos_linea)

# Creamos EDAs para trabajar con el algoritmo genetico
nodos = [] # nodos = ciudades codificadas en numeros
distancias = [] # Distancia de cada nodo con todos los demas
for dato_actual in datos:
	nodos.append(int(dato_actual[0])-1) # Insertamos los nodos
	x_actual = float(dato_actual[1])
	y_actual = float(dato_actual[2])
	# Calculo de distancia euclidea de un nodo a los demas nodos
	aux_distancias = []
	for dato_siguiente in datos:
		x_siguiente = float(dato_siguiente[1])
		y_siguiente = float(dato_siguiente[2])
		x = x_siguiente-x_actual
		x = math.pow(x,2)
		y = y_siguiente-y_actual
		y = math.pow(y,2)
		aux_distancias.append(math.sqrt(x+y))
	distancias.append(aux_distancias)


# --------------------------------------------------------------------------------------
# ALGORITMO GENETICO
# --------------------------------------------------------------------------------------
# fitness = distancia de la secuencia
def f_fitness(individuo,distancias):
	d = 0
	for i in range(0,len(individuo)-1):
		nodo_actual = individuo[i]
		nodo_siguiente = individuo[i+1]
		d = d + distancias[nodo_actual][nodo_siguiente]
	return d

# Genera una poblacion inicial de n_individuos
def generar_poblacion_incial(nodos,n_individuos):
	pob_inicial = []
	for i in range(n_individuos):
		pob = []
		for j in range(len(nodos)):
			nodo = random.randint(0,len(nodos)-1)
			while nodo in pob: # No se repiten los nodos en un individuo
				nodo = random.randint(0,len(nodos)-1)
			pob.append(nodo)
		pob.append(pob[0]) # nodo inicial = nodo final
		pob_inicial.append(pob)
	return pob_inicial

# Generar un plot de un individuo 
def generar_plot_individuo(individuo,datos):
	# Plot de la solucion obtenida
	# datos[0] = nodo; datos[1] = x; datos[2] = y 
	x = []
	y = []
	for i in individuo:
		x.append(datos[i][1])
		y.append(datos[i][2])
	plt.plot(x,y,'g-d')
	plt.show()

# Creamos la poblacion inicial
poblacion = generar_poblacion_incial(nodos,n_ind)
if modo_verbose:
	print "------------------------------------"
	print "POBLACION INICIAL"
	print "------------------------------------"
	print poblacion
# Bucle generaciones
for i in range(n_generaciones):
	if modo_verbose:
		print "------------------------------------"
		print "GENERACION ",i
		print "------------------------------------"
		print poblacion
	# Aplicamos funcion fitness a la poblacion
	puntuaciones = []
	for individuo in poblacion:
		puntuacion = f_fitness(individuo,distancias)
		if puntuacion < mejor_puntuacion:
			mejor_puntuacion = puntuacion
			mejor_individuo = individuo
		puntuaciones.append(puntuacion)
	puntuaciones_ord = sorted(puntuaciones)
	if modo_verbose:
		print "------------------------------------"
		print "PUNTUACIONES"
		print "------------------------------------"
		for j in range(len(poblacion)):
			print j,": ",puntuaciones[j]
	# Seleccion: n_padres_seleccion con menor puntuacion de fitness
	indices_padres = []
	for j in range(n_padres_seleccion):
		aux_i = 1
		aux_indice = puntuaciones.index(puntuaciones_ord[j])
		while aux_indice in indices_padres:
			aux_indice = puntuaciones.index(puntuaciones_ord[j],aux_i)
			aux_i += 1
		indices_padres.append(aux_indice)
	if modo_verbose:
		print "------------------------------------"
		print "SELECCION"
		print "------------------------------------"
		for j in indices_padres:
			print "Padre: ",j
	# Cruce: Cruce uniforme sin repetir nodos (ciudades)
	hijos_cruzados = []
	for j in range(len(indices_padres)-1):
		padre1 = poblacion[indices_padres[j]]
		padre2 = poblacion[indices_padres[j+1]]
		hijo = []
		hijo.append(padre1[0])
		p1 = 1
		p2 = 0
		while len(hijo) != len(padre1)-1: # len(padre1)-1: porque el hijo acaba con el nodo que empieza
			while (p2 < len(padre2)) and (padre2[p2] in hijo):
				p2 += 1
			if p2 < len(padre2):
				hijo.append(padre2[p2])
			while (p1 < len(padre1)) and (padre1[p1] in hijo):
				p1 += 1
			if p1 < len(padre1):
				hijo.append(padre1[p1])
		hijo.append(hijo[0]) # El nodo destino es el nodo origen
		hijos_cruzados.append(hijo)
	if modo_verbose:
		print "------------------------------------"
		print "CRUCE"
		print "------------------------------------"
		for hijo in hijos_cruzados:
			print "Hijo_cruzado: ",hijo
	# Mutacion: intercambiar dos nodos (sin tener en cuenta el inicial y el final)
	hijos = []
	pos_1 = random.randint(1,len(nodos)-2)
	pos_2 = random.randint(1,len(nodos)-2)
	while pos_2 == pos_1:
		pos_2 = random.randint(1,len(nodos)-2)
	for hijo_cruzado in hijos_cruzados:
		hijo = hijo_cruzado[:] # Copia de la lista hijo_cruzado
		hijo[pos_1] = hijo_cruzado[pos_2]
		hijo[pos_2] = hijo_cruzado[pos_1]
		hijos.append(hijo)
	if modo_verbose:
		print "------------------------------------"
		print "MUTACION"
		print "------------------------------------"
		print "Indices intercambio: ",pos_1,pos_2
		for hijo in hijos:
			print "Hijo: ",hijo
	# Remplazo
	indices_individuos_peores = []
	for j in range(len(hijos)):
		aux_i = 1
		aux_indice = puntuaciones.index(puntuaciones_ord[len(puntuaciones_ord)-1-j])
		while (aux_indice in indices_padres) or (aux_indice in indices_individuos_peores): # Coger hijos que no sean padres
			aux_indice = puntuaciones.index(puntuaciones_ord[len(puntuaciones_ord)-1-j],aux_i)
			aux_i += 1
		indices_individuos_peores.append(aux_indice)
		poblacion[aux_indice] = hijos[j]
	if modo_verbose:
		print "------------------------------------"
		print "REMPLAZO:"
		print "------------------------------------"
		print("Indices_peores_individuos:")
		for indice in indices_individuos_peores:
			print "Indice: ",indice
		print "Poblacion nueva:"
		for individuo in poblacion:
			print "Individuo: ",individuo


# --------------------------------------------------------------------------------------
# SALIDA POR PANTALLA
# --------------------------------------------------------------------------------------
# Mostramos el mejor individuo obtenido en la ejecucion
print "------------------------------------"
print "MEJOR INDIVIDUO"
print "------------------------------------"
print "Individuo: ",mejor_individuo
print "Puntuacion : ",mejor_puntuacion	

# Generamos el mejor individuo obtenido
generar_plot_individuo(mejor_individuo,datos)
