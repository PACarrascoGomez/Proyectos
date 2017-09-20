import random
import math
import xml.etree.ElementTree as ET
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#########################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: Sistemas multiagente (SMA)
# Trabajo: Entorno de negociacion automatica bilateral
# Lenguaje: python2.7
#########################################################

# NOTA: Para que funcione el programa es necesario tener
# instalados los siguiente paquetes:
#	apt-get install python-matplotlib
#	apt-get install python-tk

# Cargamos el dominio
from dominio import *

# Cargamos las funcion de utilidad
from funciones_utilidad import *

# Cargamos la funcion de concesion
from estrategias_concesion import *

# Cargamos las funcion de aceptacion
from estrategias_aceptacion import *

#--------------------------------------------------------
# IMPORTAR DATOS DE FICHERO XML
#--------------------------------------------------------
def importar_xml(fichero):
	datos = {}
	tree = ET.parse(fichero)
	root = tree.getroot()
	datos['nombre_agente'] = root[0].text # Nombre_agente
	datos['n_atributos'] = int(root[1].text) # Numero atributos
	datos['t_oferta'] = int(root[2][0].text) # Tipo de oferta
	datos['t_fu'] = int(root[3][0].text) # Tipo de funcion de utilidad
	datos['t_concesion'] = int(root[4][0].text) # Tipo de concesion
	datos['p_concesion'] = root[4][1].text.split(" ") # Parametros de concesion
	datos['s_inicial'] = float(root[4][2].text) # Concesion (s) inicial
	datos['t_aceptacion'] = float(root[5][0].text) # Criterio de aceptacion
	datos['s_aceptacion'] = float(root[5][1].text) # Concesion (s) minimo dispuesto a aceptar
	datos['tiempo'] = int(root[6].text) # Tiempo de negociacion
	return datos

#--------------------------------------------------------
# ESTRATEGIAS DE GENERACION DE OFERTAS
#--------------------------------------------------------
# Algoritmo genetico para generar ofertas
#	agente: 1 = agente1 ; 2 = agente2
#	ite: Numero de iteraciones
#	nip: Numero de individuos por poblacion
#	size_v: Numero de elementos del vector v
#	s_max: Valor de concesion actual maximo
#	s_min: Valor de concesion actual minimo
#	op: Opcion para seleccionar la oferta a devolver (1: max; 2: min; 3: random)
#	op_fu: Funcion de utilidad del agente que invoca la funcion
#	tipos_oferta: Tipos de ofertas definidos en el dominio
#	rango_valores_oferta: Valores que puede tomar cada componente de la oferta definidos en el dominio
def gen_ofertas_genetico(agente,ite,nip,size_v,s_max,s_min,op,op_fu,tipos_oferta,rango_valores_oferta):
	# Listas donde almacenamos las ofertas dentro del rango de s_actual
	ofertas_validas = []
	f_utilidad_ofertas_validas = []
	# Almacenamos la oferta mas alta para el caso de no encontrar ofertas dentro del rango
	mejor_oferta_encontrada = []
	fu_mejor_oferta_encontrada = 0
	# Generacion de la poblacion inicial
	poblacion = []
	for i in range(0,nip):
		poblacion.append(oferta_random(tipos_oferta,rango_valores_oferta))
	# Bucle (Generaciones)
	for g in range(0,ite):
		# SELECCION (Numero de padres = nip / 2)
		n_padres = nip/2
		f_utilidad_poblacion = []
		f_utilidad_poblacion_ord = []
		for i in range(0,nip):
			f_u = funcion_utilidad(agente,op_fu,poblacion[i])
			f_utilidad_poblacion.append(f_u)
			f_utilidad_poblacion_ord.append(f_u)
		f_utilidad_poblacion_ord.sort(reverse=True)
		# Actualizamos la mejor oferta
		if(f_utilidad_poblacion_ord[0] > fu_mejor_oferta_encontrada):
			fu_mejor_oferta_encontrada = f_utilidad_poblacion_ord[0]
			indice = f_utilidad_poblacion.index(fu_mejor_oferta_encontrada)
			mejor_oferta_encontrada = poblacion[indice]
		# Actualizamos las ofertas validas
		i = 0
		while(i < nip and f_utilidad_poblacion_ord[i] >= s_min):
			if(f_utilidad_poblacion_ord[i] <= s_max):
				f_utilidad_ofertas_validas.append(f_utilidad_poblacion_ord[i])
				indice = f_utilidad_poblacion.index(f_utilidad_poblacion_ord[i])
				ofertas_validas.append(poblacion[indice])
			i += 1
		padres = []
		for i in range(0,n_padres):
			f_u = f_utilidad_poblacion_ord[i]
			indice = f_utilidad_poblacion.index(f_u)
			padres.append(poblacion[indice])
		# CRUCE (Cruce aleatorio por atributos)
		hijos = []
		for i in range(0,n_padres):
			n_atributos_a_cambiar = random.randint(1,size_v)
			indices_atributos_a_cambiar = []
			for j in range(0,n_atributos_a_cambiar):
				indices_atributos_a_cambiar.append(random.randint(0,size_v-1))
			hijo = []
			if(i == n_padres-1): # Cruce del ultimo con el primero
				hijo = padres[i][:]
				for j in range(0,n_atributos_a_cambiar):
					aux_indice = indices_atributos_a_cambiar[j]
					hijo[aux_indice] = padres[0][aux_indice]
			else:
				hijo = padres[i][:]
				for j in range(0,n_atributos_a_cambiar):
					aux_indice = indices_atributos_a_cambiar[j]
					hijo[aux_indice] = padres[i+1][aux_indice]
			hijos.append(hijo)
		# MUTACION (Intercambio aleatorio de un elemento de la oferta)
		for i in range(0,len(hijos)):
			aux_indice = random.randint(0,size_v-1)
			valor_aleatorio_oferta_indice = elemento_oferta_random(tipos_oferta,rango_valores_oferta,aux_indice)
			hijos[i][aux_indice] = valor_aleatorio_oferta_indice
		# REMPLAZO
		indices_remplazo = []
		e_max = nip-1
		e_min = e_max-len(hijos)
		j = 0
		for i in range(e_max,e_min,-1):
			f_u = f_utilidad_poblacion_ord[i]
			indice = f_utilidad_poblacion.index(f_u)
			poblacion[indice] = hijos[j]
			j += 1
	# Comprobamos si el algoritmo genetico a generado alguna oferta valida
	if(len(ofertas_validas)>0):
		# Seleccionamos una oferta segun la opcion escogida
		f_utilidad_ofertas_validas_ord = f_utilidad_ofertas_validas[:]
		# Mejor oferta
		if(op == 1):
			f_utilidad_ofertas_validas_ord.sort(reverse=True)
			f_utilidad_oferta = f_utilidad_ofertas_validas_ord[0]
			indice = f_utilidad_ofertas_validas.index(f_utilidad_oferta)
			oferta = ofertas_validas[indice]
		# Peor oferta
		elif(op == 2):
			f_utilidad_ofertas_validas_ord.sort()
			f_utilidad_oferta = f_utilidad_ofertas_validas_ord[0]
			indice = f_utilidad_ofertas_validas.index(f_utilidad_oferta)
			oferta = ofertas_validas[indice]
		# Oferta aleatoria
		else:
			n_random = random.randint(0,len(ofertas_validas)-1)
			f_utilidad_oferta = f_utilidad_ofertas_validas_ord[n_random]
			indice = f_utilidad_ofertas_validas.index(f_utilidad_oferta)
			oferta = ofertas_validas[indice]
	else: # Si no hay ofertas validas devolvemos una oferta cuya f_utilidad > s_max
		  # Si existe buscamos la oferta mas cercana a s_max
		max_ofertas = []
		fu_max_ofertas = []
		fu_max_ofertas_ord = []
		for aux_oferta in poblacion:
			aux_fu_oferta = funcion_utilidad(agente,op_fu,aux_oferta)
			if(aux_fu_oferta >= s_max):
				max_ofertas.append(aux_oferta)
				fu_max_ofertas.append(aux_fu_oferta)
				fu_max_ofertas_ord.append(aux_fu_oferta)
		if(len(fu_max_ofertas_ord) > 0):
			fu_max_ofertas_ord.sort()
			indice = fu_max_ofertas.index(fu_max_ofertas_ord[0])
			f_utilidad_oferta = fu_max_ofertas[indice]
			oferta = max_ofertas[indice]
		# Si no hay ninguna oferta cuya f_utilidad > s_max devolvemos
		# la mejor oferta encontrada en el genetico
		else:
			oferta = mejor_oferta_encontrada
			f_utilidad_oferta = fu_mejor_oferta_encontrada
	# Devolvemos la mejor oferta
	return (oferta,f_utilidad_oferta)

# Generacion de ofertas aleatorias
def oferta_random(tipos,rango_valores):
	oferta = []
	for i in range(0,len(tipos)):
		if(tipos[i] == "int"): # Cota superior
			oferta.append(random.randint(1,rango_valores[i]))
		elif(tipos[i] == "float"): # Cota superior
			oferta.append(random.uniform(1.0,rango_valores[i]))
		else: # Tipo list
			e_l = len(rango_valores[i])
			indice = random.randint(0,e_l-1)
			oferta.append(rango_valores[i][indice])
	return oferta

# Generacion de un elemento concreto de la oferta indicado por su indice
def elemento_oferta_random(tipos,rango_valores,i):
	elemento_oferta = ""
	if(tipos[i] == "int"): # Cota superior
		elemento_oferta = random.randint(0,rango_valores[i])
	elif(tipos[i] == "float"): # Cota superior
		elemento_oferta = random.uniform(0.0,rango_valores[i])
	else: # Tipo list
		e_l = len(rango_valores[i])
		indice = random.randint(0,e_l-1)
		elemento_oferta = rango_valores[i][indice]
	return elemento_oferta

#--------------------------------------------------------
# GRAFICA
#--------------------------------------------------------
fig, ax = plt.subplots()

# Leyendas de los ejes X e Y
tree = ET.parse("agente1.xml")
root = tree.getroot()
plt.xlabel(root[0].text)
tree = ET.parse("agente2.xml")
root = tree.getroot()
plt.ylabel(root[0].text)

# Rangos de valores de los ejes X e Y
ax.set_ylim(0, 1)
ax.set_xlim(0, 1) 

# Mostrar rejilla
ax.grid()

# Listas para x e y
xdata_agente1, ydata_agente1 = [], []
xdata_agente2, ydata_agente2 = [], []

# Funcion que actualiza la animacion del plot
def run(data):
	x, y, agente = data
	if(agente == 1):
		xdata_agente1.append(x)
		ydata_agente1.append(y)
	else:
		xdata_agente2.append(x)
		ydata_agente2.append(y)
	ax.plot(xdata_agente1, ydata_agente1, 'r-')
	ax.plot(xdata_agente2, ydata_agente2, 'b-')

#--------------------------------------------------------
# FUNCION QUE LANZA LA NEGOCIACION ENTRE 2 AGENTES
#--------------------------------------------------------

def negociacion():
	# Configuracion agente2
	xml_agente1 = "agente1.xml"
	datos_agente1 = importar_xml(xml_agente1)
	s_agente1 = datos_agente1['s_inicial']
	agente1_ofertas_recibidas = []
	agente1_ofertas_emitidas = []

	# Configuracion agente2
	xml_agente2 = "agente2.xml"
	datos_agente2 = importar_xml(xml_agente2)
	s_agente2 = datos_agente2['s_inicial']
	agente2_ofertas_recibidas = []
	agente2_ofertas_emitidas = []

	# Variable para trabajar con tiempo
	# NOTA: Trabajamos con segundos
	t_inicial = datetime.now()

	# Flag para finalizar la negociacion
	fin_negociacion_agente1 = False
	fin_negociacion_agente2 = False

	# Flag para gestionar los turnos
	turno=0

	# Numero de ofertas generadas por ambas partes en total
	n_ofertas = 0

	# Fin de la negociacion deficina por un deadline o por un acuerdo
	while(fin_negociacion_agente1 == False and fin_negociacion_agente2 == False):
		if(turno == 0): # Inicio de la negociacion
			# El agente 1 genera la oferta inicial para empezar la negociacion
			(oferta,fu_o_a1) = gen_ofertas_genetico(1,1000,5,datos_agente1['n_atributos'],s_agente1+0.1,s_agente1,datos_agente1['t_oferta'],datos_agente1['t_fu'],dominio()[0],dominio()[1])
			agente1_ofertas_emitidas.append(oferta)
			turno = 2
			n_ofertas += 1
			print "############################################################################"
			print "Sentido (oferta)\t\tf_utilidad_emisor\tf_utilidad_receptor"
			print "############################################################################"
			print "------------------------------------------------------------------------"
			print datos_agente1['nombre_agente']," --> ",datos_agente2['nombre_agente'],"\t\t",fu_o_a1,"\t\t\t",funcion_utilidad(2,datos_agente2['t_fu'],oferta),"\t"
			print "------------------------------------------------------------------------"
			#-----------------------------------------
			# Actualizamos los valores de la grafica
			#-----------------------------------------
			fu_oferta = funcion_utilidad(1,datos_agente1['t_fu'],oferta)
			fu_oferta2 = funcion_utilidad(2,datos_agente2['t_fu'],oferta)
			yield fu_oferta, fu_oferta2, 1
		# Regateo: Intercambio de ofertas de Rubinstein
		elif(turno == 1):  # Agente 1
			fu_oferta = funcion_utilidad(1,datos_agente1['t_fu'],oferta)
			agente1_ofertas_recibidas.append(oferta)
			s_agente1 = actualizar_concesion(1,datos_agente1['t_fu'],datos_agente1['t_concesion'],datos_agente1['tiempo'],agente1_ofertas_emitidas,agente1_ofertas_recibidas,datos_agente1['p_concesion'],t_inicial)
			t_actual = datetime.now()
			t = t_actual - t_inicial
			t = t.seconds
			lista_aceptar = aceptacion(1,datos_agente1['t_aceptacion'],fu_oferta,s_agente1,datos_agente1['s_aceptacion'],agente1_ofertas_emitidas,agente1_ofertas_recibidas)
			if(t >= datos_agente1['tiempo']):
				fin_negociacion_agente1 = True
				print "Se ha agotado el tiempo del agente 1 (Deadline = ",t,"s)"
			# Comporbacion aceptacion de la oferta
			elif(len(lista_aceptar) > 0):
				if(lista_aceptar[0] == True):
					fin_negociacion_agente1 = True
					print "----------------------------------"
					print "El agente 1 acepta la oferta"
					print "----------------------------------"
					print "Criterio: ", lista_aceptar[1]
					print "Oferta: ",oferta
					print "Funcion utilidad: ",fu_oferta
					print "Concesion: ",s_agente1
					#-----------------------------------------
					# Actualizamos los valores de la grafica
					#-----------------------------------------
					fu_oferta = funcion_utilidad(1,datos_agente1['t_fu'],oferta)
					fu_oferta2 = funcion_utilidad(2,datos_agente2['t_fu'],oferta)
					yield fu_oferta, fu_oferta2, 1
				elif(lista_aceptar[0] == False and lista_aceptar[2] == ""):
					fin_negociacion_agente1 = True
					print "----------------------------------------"
					print "El agente 1 no ha llegado a un acuerdo"
					print "----------------------------------------"
					print "Criterio: ", lista_aceptar[1]
				elif(lista_aceptar[0] == False and lista_aceptar[2] != ""):
					oferta = lista_aceptar[2]
					agente1_ofertas_emitidas.append(oferta)
					turno = 2
					n_ofertas += 1
					print datos_agente1['nombre_agente']," --> ",datos_agente2['nombre_agente'],"\t\t",fu_o_a1,"\t\t\t",funcion_utilidad(2,datos_agente2['t_fu'],oferta),"\t"
					print "------------------------------------------------------------------------"
					#-----------------------------------------
					# Actualizamos los valores de la grafica
					#-----------------------------------------
					fu_oferta = funcion_utilidad(1,datos_agente1['t_fu'],oferta)
					fu_oferta2 = funcion_utilidad(2,datos_agente2['t_fu'],oferta)
					yield fu_oferta, fu_oferta2, 1
			else:
				(oferta,fu_o_a1) = gen_ofertas_genetico(1,1000,5,datos_agente1['n_atributos'],s_agente1+0.1,s_agente1,datos_agente1['t_oferta'],datos_agente1['t_fu'],dominio()[0],dominio()[1])
				agente1_ofertas_emitidas.append(oferta)
				turno = 2
				n_ofertas += 1
				print datos_agente1['nombre_agente']," --> ",datos_agente2['nombre_agente'],"\t\t",fu_o_a1,"\t\t\t",funcion_utilidad(2,datos_agente2['t_fu'],oferta),"\t"
				print "------------------------------------------------------------------------"
				#-----------------------------------------
				# Actualizamos los valores de la grafica
				#-----------------------------------------
				fu_oferta = funcion_utilidad(1,datos_agente1['t_fu'],oferta)
				fu_oferta2 = funcion_utilidad(2,datos_agente2['t_fu'],oferta)
				yield fu_oferta, fu_oferta2, 1
			#-----------------------------------------
		else: # Agente 2
			fu_oferta = funcion_utilidad(2,datos_agente2['t_fu'],oferta)
			agente2_ofertas_recibidas.append(oferta)
			s_agente2 = actualizar_concesion(2,datos_agente2['t_fu'],datos_agente2['t_concesion'],datos_agente2['tiempo'],agente2_ofertas_emitidas,agente2_ofertas_recibidas,datos_agente2['p_concesion'],t_inicial)
			t_actual = datetime.now()
			t = t_actual - t_inicial
			t = t.seconds
			lista_aceptar = aceptacion(2,datos_agente2['t_aceptacion'],fu_oferta,s_agente2,datos_agente2['s_aceptacion'],agente2_ofertas_emitidas,agente2_ofertas_recibidas)
			if(t >= datos_agente2['tiempo']):
				fin_negociacion_agente2 = True
				print "Se ha agotado el tiempo del agente 2 (Deadline = ",t,"s)"
			# Comporbacion aceptacion de la oferta
			elif(len(lista_aceptar) > 0):
				if(lista_aceptar[0] == True):
					fin_negociacion_agente2 = True
					print "----------------------------------"
					print "El agente 2 acepta la oferta"
					print "----------------------------------"
					print "Criterio: ", lista_aceptar[1]
					print "Oferta: ",oferta
					print "Funcion utilidad: ",fu_oferta
					print "Concesion: ",s_agente2
					#-----------------------------------------
					# Actualizamos los valores de la grafica
					#-----------------------------------------
					fu_oferta = funcion_utilidad(2,datos_agente2['t_fu'],oferta)
					fu_oferta2 = funcion_utilidad(1,datos_agente1['t_fu'],oferta)
					yield fu_oferta2, fu_oferta, 2
				elif(lista_aceptar[0] == False and lista_aceptar[2] == ""):
					fin_negociacion_agente2 = True
					print "----------------------------------------"
					print "El agente 2 no ha llegado a un acuerdo"
					print "----------------------------------------"
					print "Criterio: ", lista_aceptar[1]
				elif(lista_aceptar[0] == False and lista_aceptar[2] != ""):
					oferta = lista_aceptar[2]
					agente2_ofertas_emitidas.append(oferta)
					turno = 1
					n_ofertas += 1
					print datos_agente2['nombre_agente']," --> ",datos_agente1['nombre_agente'],"\t\t",fu_o_a2,"\t\t\t",funcion_utilidad(1,datos_agente1['t_fu'],oferta),"\t"
					print "------------------------------------------------------------------------"
					#-----------------------------------------
					# Actualizamos los valores de la grafica
					#-----------------------------------------
					fu_oferta = funcion_utilidad(2,datos_agente2['t_fu'],oferta)
					fu_oferta2 = funcion_utilidad(1,datos_agente1['t_fu'],oferta)
					yield fu_oferta2, fu_oferta, 2
			else:
				(oferta,fu_o_a2) = gen_ofertas_genetico(2,1000,5,datos_agente2['n_atributos'],s_agente2+0.1,s_agente2,datos_agente2['t_oferta'],datos_agente2['t_fu'],dominio()[0],dominio()[1])
				agente2_ofertas_emitidas.append(oferta)
				turno = 1
				n_ofertas += 1
				print datos_agente2['nombre_agente']," --> ",datos_agente1['nombre_agente'],"\t\t",fu_o_a2,"\t\t\t",funcion_utilidad(1,datos_agente1['t_fu'],oferta),"\t"
				print "------------------------------------------------------------------------"
				#-----------------------------------------
				# Actualizamos los valores de la grafica
				#-----------------------------------------
				fu_oferta = funcion_utilidad(2,datos_agente2['t_fu'],oferta)
				fu_oferta2 = funcion_utilidad(1,datos_agente1['t_fu'],oferta)
				yield fu_oferta2, fu_oferta, 2
			#-----------------------------------------
	print "Numero de ofertas generadas: ",n_ofertas
	

# Animacion
ani = animation.FuncAnimation(fig, run, frames=negociacion, init_func=negociacion, blit=False, interval=10, repeat=False)

# # Ploteamos
plt.show()

