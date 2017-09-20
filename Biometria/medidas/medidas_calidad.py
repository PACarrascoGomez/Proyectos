import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

############################################
# Autor: Pascual Andres Carrasco Gomez
# Entorno: python2.7
# Descripcion:
#	- Curva ROC
#	- FP(FN = X) y umbral
#	- FN(FP = X) y umbral
#	- FP = FN y umbral
#	- Area bajo la curva ROC
#	- D-Prime
# Nota: El programa requiere:
#	apt-get install python-matplotlib
#	apt-get install python-tk
############################################

#-------------------------------------------
# Parametros
#-------------------------------------------
if len(sys.argv) != 3:
	print("Uso: python2.7 medidas_calidad <scores_clientes> <scores_impostores>")
	sys.exit(1)

#-------------------------------------------
# Funciones
#-------------------------------------------
# Retorna una lista con los scores del fichero f_scores
# f_scores: fichero que contiene los scores
# op: Opcion que puede tomar dos valores:
#		1: cliente
#		2: impostor
def cargar_scores(f_scores,op):
	scores = []
	f = open(f_scores,"r")
	for line in f:
		s = line.split("\n")[0].split(" ")[1]
		scores.append((float(s),op))
	return scores

# Imprime el menu por terminal
def mostrar_menu():
	print "------------------------------------"
	print "\t\tMENU"
	print "------------------------------------"
	print "1) Curva ROC"
	print "2) FP(FN = X) y umbral"
	print "3) FN(FP = X) y umbral"
	print "4) FP = FN y umbral"
	print "5) Area bajo la curva ROC"
	print "6) D-Prime"
	print "7) Salir"

# Funcion h (AROC)
# x = score_cliente - score_impostor
def h(x):
	r = 0
	if x > 0:
		r = 1.0
	elif x == 0:
		r = 0.5
	else:
		r = 0.0
	return r

#-------------------------------------------
# Main
#-------------------------------------------
# Cargamos los scores de clientes e impostores
scores_clientes = cargar_scores(sys.argv[1],1)
scores_impostores = cargar_scores(sys.argv[2],2)

# Obtenemos los datos de la curva ROC
# Ordenamos todos los scores de menor a mayor
scores = scores_clientes + scores_impostores
scores.sort(key=lambda t: t[0])
scores = [(0.0,0)] + scores + [(1.0,0)]

# Valores de la grafica
x = [] # FP
y = [] # 1-FN
q_c = 0
q_i = 0
for i in range(0,len(scores)):
	acceso = scores[i][1]
	if acceso == 1: # cliente
		q_c += 1
	elif acceso == 2: # impostor
		q_i += 1
	x.append((len(scores_impostores)-q_i)/float(len(scores_impostores)))
	y.append(1-(q_c/float(len(scores_clientes))))

# Bucle de iteracion con el usuario
op = -1
while op != 7:
	mostrar_menu()
	op = input("Escoge una opcion: [1-7]\n")
	while op < 1 or op > 7:
		mostrar_menu()
		op = input("Escoge una opcion: [1-7]\n")
	
	# Curva ROC
	if op == 1:
		# Grafica (plot)
		plt.xlabel('FP')
		plt.ylabel('1-FN')
		plt.title('Curva ROC')
		plt.plot(x,y)
		plt.show()

	# FP(FN = X) y umbral
	elif op == 2:
		fn = input("Introduce un valor para FN: [0.0-1.0]\n")
		indice = -1
		d_min = float("Inf")
		for i in range(0,len(y)):
			if abs(y[i]-fn) < d_min:
				indice = i
				d_min = abs(y[i]-fn)
		print "FP(FN=" + str(fn) + "):",x[indice]
		print "FN: ",1-y[indice]
		print "umbral:",scores[indice][0]

	# FN(FP = X) y umbral
	elif op == 3:
		fp = input("Introduce un valor para FP: [0.0-1.0]\n")
		indice = -1
		d_min = float("Inf")
		for i in range(0,len(x)):
			if abs(x[i]-fp) < d_min:
				indice = i
				d_min = abs(x[i]-fp)
		print "FN(FP=" + str(fp) + "):",(1.0-y[indice])
		print "FP:", x[indice]
		print "umbral:",scores[indice][0]

	# FP = FN y umbral
	elif op == 4:
		indice = -1
		d_min = float("Inf")
		for i in range(0,len(x)):
			if abs(x[i]-(1-y[i])) < d_min:
				indice = i
				d_min = abs(x[i]-(1-y[i]))
		print "FP: ",x[indice]
		print "FN: ",1-y[indice]
		print "umbral: ",scores[indice][0]


	# Area bajo la curva ROC
	elif op == 5:
		aux_suma = 0.0
		for s_c in scores_clientes:
			for s_i in scores_impostores:
				aux_suma += h(s_c[0]-s_i[0])
		aroc = (1.0/(len(scores_clientes)*len(scores_impostores)))*aux_suma
		print "AROC: ",aroc

	# d-prime
	elif op == 6:
		m_clientes = 0 # media clientes
		for score in scores_clientes:
			m_clientes += score[0]
		m_clientes = m_clientes/float(len(scores_clientes)) 
		dt_clientes = 0 # Desviacion tipica clientes
		for score in scores_clientes:
			aux = (score[0]-m_clientes)*(score[0]-m_clientes)
			dt_clientes += aux
		dt_clientes = dt_clientes/len(scores_clientes)
		m_impostores = 0 # media impostores
		for score in scores_impostores:
			m_impostores += score[0]
		m_impostores = m_impostores/float(len(scores_impostores)) 
		dt_impostores = 0 # Desviacion tipica impostores
		for score in scores_impostores:
			aux = (score[0]-m_impostores)*(score[0]-m_impostores)
			dt_impostores += aux
		dt_impostores = dt_impostores/len(scores_impostores)
		dprime = (m_clientes-m_impostores)/math.sqrt(dt_clientes+dt_impostores)
		print "D-Prime: ",dprime