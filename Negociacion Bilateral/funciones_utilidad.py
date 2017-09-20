import math
from preferencias_agente1 import * # w_agente1(), v_agente1(oferta)
from preferencias_agente2 import * # w_agente2(), v_agente2(oferta)

#########################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: Sistemas multiagente (SMA)
# Trabajo: Entorno de negociacion automatica bilateral
# Descripcion: Modulo con las funciones de utilidad
# Lenguaje: python2.7
#########################################################

# GESTIONAR FUNCIONES DE UTILIDAD
# Para introducir una funcion de utilidad nueva insertar una opcion nueva
# agente: 1 = Agente1 ; 2 = Agente2
# opcion: opcion para elegir la funcion de utilidad a utilizar
# oferta: oferta a la cual se le aplica la funcion de utilidad
def funcion_utilidad(agente,opcion,oferta):
	if(agente == 1):
		w = w_agente1()
		v = v_agente1(oferta)
	else: # agente == 2
		w = w_agente2()
		v = v_agente2(oferta)
	if(opcion == 1):
		#--------------------------------------------------------
		# FUNCION DE UTILIDAD LINEAL
		#--------------------------------------------------------
		aux = 0
		for i in range(0,len(w)):
			aux += w[i]*v[i]
		return aux
	elif(opcion == 2):
		#--------------------------------------------------------
		# FUNCION DE UTILIDAD TIPO 2 (Solo para probar el modulo)
		#--------------------------------------------------------
		aux = 0
		for i in range(0,len(w)):
			aux += (w[i]*(v[i]/2.0))+0.05
		return aux
	# elif(opcion == 3):
	# elif(opcion == 4):
	# elif(opcion == 5):
	# ...
	return 0