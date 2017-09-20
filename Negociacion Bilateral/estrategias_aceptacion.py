
#########################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: Sistemas multiagente (SMA)
# Trabajo: Entorno de negociacion automatica bilateral
# Descripcion: Modulo con los criterios de aceptacion
# Lenguaje: python2.7
#########################################################

# GESTIONAR CRITERIOS DE ACEPTACION
# Para introducir una funcion de aceptacion nueva insertar una opcion nueva
# agente: 1 = Agente1 ; 2 = Agente2
# opcion: opcion para elegir la funcion de aceptacion a utilizar
# fu_oferta: funcion de utilidad de la oferta
# s_actual: concesion actual del agente
# s_aceptacion: concesion minima a la que esta dispuesto el agente a llegar
# ofertas_a: lista con todas las ofertas emitidas por el agente
# ofertas_b: lista con todas las ofertas recibidas por el agente
# NOTA: El retorno de la funcion debe ser una lista de tres componentes
#		return[0]: bool si aceptamos o no la oferta
#		return[1]: un mensaje que se mostrara por pantalla
#		return[2]: una oferta de contestacion ; "" en caso de no devolver ninguna oferta
#		Cualquier otro caso retorna lista vacia
def aceptacion(agente,opcion,fu_oferta,s_actual,s_aceptacion,ofertas_a,ofertas_b):
	if(opcion == 1):
		#--------------------------------------------------------
		# FUNCION DE ACEPTACION BASICA
		#--------------------------------------------------------
		if(fu_oferta > s_actual):
			mensaje = "Se cumple fu_oferta > s_actual"
			return [True,mensaje,""]
		else:
			if(s_actual < s_aceptacion):
				mensaje = "No se ha llegado a un acuerdo: s_actual < s_aceptacion"
				return [False,mensaje,""]
	elif(opcion == 2):
		#--------------------------------------------------------
		# FUNCION DE ACEPTACION AVANZADA
		#--------------------------------------------------------
		if(s_actual < s_aceptacion):
			# Elegimos la mejor oferta que nos ha enviado el adversario
			from funciones_utilidad import *
			# NOTA: escogemos la opcion de fu_lineal como podriamos haber escogido otra
			fu_ofertas_b = []
			fu_ofertas_b_ord = []
			for o in ofertas_b:
				fu_ofertas_b.append(funcion_utilidad(agente,1,o))
				fu_ofertas_b_ord.append(funcion_utilidad(agente,1,o))
			fu_ofertas_b_ord.sort(reverse=True) # Ordenamos de mayor a menor
			indice = fu_ofertas_b.index(fu_ofertas_b_ord[0])
			oferta = ofertas_b[indice]
			# Si la oferta mas alta es mayor que s_aceptacion -> enviamos la mejor oferta recibida
			if(fu_ofertas_b_ord[0] > s_aceptacion):
				mensaje = "El agente ",agente," envia la mejor oferta recibida hasta el momento"
				return [False,mensaje,oferta]
			# Si no, no llegamos a un acuerdo
			else:
				mensaje = "No se ha llegado a un acuerdo: fu_mejor_oferta < s_aceptacion"
				return [False,mensaje,""]
		elif(fu_oferta > s_actual):
			mensaje = "Se cumple fu_oferta > s_actual"
			return [True,mensaje,""]
	# elif(opcion == 3):
	# elif(opcion == 4):
	# elif(opcion == 5):
	# ...
	return []