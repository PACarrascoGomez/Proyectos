import sys
import math
import random
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------------------
# Algoritmo Enfriamiento Simulado
# --------------------------------------------------------------------------------------
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TIA
# Problema: Viajante de comercio
# Lenguaje: python2.7

# --------------------------------------------------------------------------------------
# PARAMETROS DEL ALGORITMO
# --------------------------------------------------------------------------------------
# Comprobacion de parametros de entrada
if len(sys.argv) != 7:
 	print "------------------------------------------------------------------------------------------"
 	print "Uso: python2.7 viajante_vecinos.py <f_tsp> <n_ite> <T> <k> <n_vecinos> <verbose>"
 	print "------------------------------------------------------------------------------------------"
 	print "<f_tsp>: Fichero con las coordenadas del problema TSP (string)"
 	print "<n_ite>: Iteraciones en el bucle (int)"
 	print "<T>: Valor de Temperatura (float)"
 	print "<k>: Factor k para decrementar temperatura [0...1]     (float)"
 	print "<n_vecinos>: Cantidad de sucesores para la solucion actual (int)"
 	print "<verbose>: Verbose por pantalla (boolean)"
 	sys.exit(0)

# Parametros generales para el algoritmo enfriamiento simulado
f_tsp = sys.argv[1]
n_ite = int(sys.argv[2])
T = float(sys.argv[3])
k = float(sys.argv[4])
n_vecinos = int(sys.argv[5])
modo_verbose = True if sys.argv[6] == "True" else False

# --------------------------------------------------------------------------------------
# GENERACION DE EDAs PARA EL ALGORITMO
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
# ALGORITMO ENFRIAMIENTO SIMULADO
# --------------------------------------------------------------------------------------
# fitness = distancia de la secuencia
def f_fitness(individuo,distancias):
	d = 0
	for i in range(0,len(individuo)-1):
		nodo_actual = individuo[i]
		nodo_siguiente = individuo[i+1]
		d = d + distancias[nodo_actual][nodo_siguiente]
	return d

# Genera un individuo (solucion) de forma aleatoria
def generar_solucion(nodos):
	individuo = []
	for j in range(len(nodos)):
		nodo = random.randint(0,len(nodos)-1)
		while nodo in individuo: # No se repiten los nodos en un individuo
			nodo = random.randint(0,len(nodos)-1)
		individuo.append(nodo)
	individuo.append(individuo[0])
	return individuo

# Genera n_vecinos a partir de la s_actual
def generar_vecinos(s_actual,n_vecinos):
	lista_vecinos = []
	particion = int(round(len(s_actual)/2))
	for i in range(n_vecinos):
		vecino = []
		vecino += s_actual[particion:len(s_actual)-1]
		vecino += s_actual[0:particion]
		# Intercambio reciproco de dos nodos aleatorios
		pos1 = random.randint(0,len(s_actual)-2)
		pos2 = random.randint(0,len(s_actual)-2)
		while pos2 == pos1:
			pos2 = random.randint(0,len(s_actual)-2)
		aux = vecino[pos1]
		vecino[pos1] = vecino[pos2]
		vecino[pos2] = aux
		# El nodo inicial ha de ser igual al final
		vecino.append(vecino[0])
		lista_vecinos.append(vecino)
	return lista_vecinos

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

# --------------------------------------------------------------------------------------
# ALGORITMO ENFRIAMIENTO SIMULADO
# --------------------------------------------------------------------------------------
s_actual = generar_solucion(nodos)
s_mejor = s_actual
puntuacion_s_mejor = f_fitness(s_mejor,distancias)
I = 0
# Bucle Principal
while I < n_ite:
	I = I+1
	if modo_verbose:
		print "------------------------------------"
		print "S_ACTUAL:"
		print "------------------------------------"
		print s_actual 
	# s_nuevo a partir de los vecinos de s_actual
	vecinos = generar_vecinos(s_actual,n_vecinos)
	fitness_vecinos = []
	for vecino in vecinos:
		fitness_vecinos.append(f_fitness(vecino,distancias))
	fitness_vecinos_ord = sorted(fitness_vecinos) # Ordena de menor a mayor
	if modo_verbose:
		print "------------------------------------"
		print "VECINOS:"
		print "------------------------------------"
		print vecinos
		print "------------------------------------"
		print "FITNESS VECINOS:"
		print "------------------------------------"
		print fitness_vecinos
	# Nos quedamos con 1/3 de los mejores vecinos (min f_fitness)
	particion = int(round(len(vecinos)/3.0))
	vecinos_candidatos = []
	for j in range(particion):
		vecinos_candidatos.append(vecinos[fitness_vecinos.index(fitness_vecinos_ord[j])])
	if modo_verbose:
		print "------------------------------------"
		print "VECINOS CANDIDATOS:"
		print "------------------------------------"
		print vecinos_candidatos
	# De los vecinos seleccionados (candidatos) escogemos uno aleatorio
	indice_aleatorio = random.randint(0,len(vecinos_candidatos)-1)
	s_nuevo = vecinos_candidatos[indice_aleatorio]
	if modo_verbose:
		print "------------------------------------"
		print "VECINO SELECCIONADO (S_NUEVO):"
		print "------------------------------------"
		print "Indice aleatorio: ",indice_aleatorio
		print "vecino seleccionado (s_nuevo): ",s_nuevo
	probabilidad = ""
	incr_f =  f_fitness(s_actual,distancias) - f_fitness(s_nuevo,distancias)
	if incr_f > 0: # mejora la solucion
		s_actual = s_nuevo
		if f_fitness(s_nuevo,distancias) < puntuacion_s_mejor:
			s_mejor = s_nuevo
			puntuacion_s_mejor = f_fitness(s_nuevo,distancias)
	else:
		if (T > 0): # Si T es 0 no se acepta directamente
			# Calculamos la probabilidad = e^(incr_f/T)
			e = math.e
			incr_f = round(incr_f,4) # Nos quedamos con 4 decimales
			incr_f = math.sqrt(incr_f*-1)*-1 # Tratamos los datos
			probabilidad = math.pow(e,(incr_f/T))
			probabilidad = round(probabilidad,4) # Nos quedamos con 4 decimales
			v_aleatorio = random.random(); # Valor entre 0.0 y 1.0
			if probabilidad > v_aleatorio: # nos quedamos con la solucion
				s_actual = s_nuevo
				# Decrementamos la Temperatura
				T = round(k*T,4) # Nos quedamos con 4 decimales
	if modo_verbose:
		print "------------------------------------"
		print "PARAMETROS:"
		print "------------------------------------"
		print "INCREMENTO_F: ", incr_f
		print "Temperatura: ", T
		print "Probabilidad: ", probabilidad


# --------------------------------------------------------------------------------------
# SALIDA POR PANTALLA
# --------------------------------------------------------------------------------------
# Mostramos el mejor individuo obtenido en la ejecucion
print "------------------------------------"
print "MEJOR INDIVIDUO"
print "------------------------------------"
print "Individuo: ",s_mejor
print "Puntuacion : ",puntuacion_s_mejor

# Generamos el mejor individuo obtenido
generar_plot_individuo(s_mejor,datos)
