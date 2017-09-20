import math
from datetime import datetime
from funciones_utilidad import *

#########################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: Sistemas multiagente (SMA)
# Trabajo: Entorno de negociacion automatica bilateral
# Descripcion: Modulo con las estrategias de concesion
# Lenguaje: python2.7
#########################################################

# GESTIONAR FUNCIONES DE CONCESION
# Para introducir una funcion de concesion nueva insertar una opcion nueva
# agente: 1 = Agente1 ; 2 = Agente2
# tipo_fu: Funcion de utilidad que utiliza el agente
# opcion: opcion para elegir la funcion de concesion a utilizar
# T_agente: Tiempo de negociacion del agente
# ofertas_a: lista con todas las ofertas emitidas por el agente
# ofertas_b: lista con todas las ofertas recibidas por el agente
# parametros: conjunto de parametros necesarios para calcular la funcion de concesion
# t_inicial: Tiempo de inicio de las negociaciones
# NOTA: Los parametros son los valores introducidos en parametros de concesion del xml del agente
def actualizar_concesion(agente,tipo_fu,opcion,T_agente,ofertas_a,ofertas_b,parametros,t_inicial):
	if(opcion == 1):
		#--------------------------------------------------------
		# TEMPORAL
		#--------------------------------------------------------
		#	0 < B < 1 = Boulware
		#	1 < B < inf = Conceder
		#--------------------------------------------------------
		# Parametros
		RU = float(parametros[0])
		B = float(parametros[1])
		exponente = 1.0/B
		t_actual = datetime.now()
		t = t_actual - t_inicial
		t = float(t.seconds)
		s = 1 - ((1 - RU)*(math.pow((t/T_agente),exponente)))
		return s
	elif(opcion == 2):
		#--------------------------------------------------------
		# COMPORTAMIENTO
		#--------------------------------------------------------
		# Basada en el comportamiento (a agente que llama a la funcion)
		#							  (b agente destinatario)
		#--------------------------------------------------------
		#def concesion_comportamiento(agente,tipo,RU,D,ofertas_a,ofertas_b):
		# Parametros
		RU = float(parametros[0])
		D = int(parametros[1])
		tipo = parametros[2]
		if(len(ofertas_b) >= D and len(ofertas_a) >= 1): # Concesion por comportamiento
			s = 0
			if(agente == 1):
				# Obtenemos los valores w_agente y v_agente
				from preferencias_agente1 import *
				fu_oferta_ab_t_1 = funcion_utilidad(1,tipo_fu,ofertas_a[len(ofertas_a)-1])
				fu_oferta_ba_t_1 = funcion_utilidad(1,tipo_fu,ofertas_b[len(ofertas_b)-1])
				fu_oferta_ba_t_D = funcion_utilidad(1,tipo_fu,ofertas_b[len(ofertas_b)-D])
				if(D == 1):
					return 1
				else:
					fu_oferta_ba_t_D_1 = funcion_utilidad(1,tipo_fu,ofertas_b[len(ofertas_b)-D+1])
			else: # agente 2
				# Obtenemos los valores w_agente y v_agente
				from preferencias_agente2 import *
				fu_oferta_ab_t_1 = funcion_utilidad(2,tipo_fu,ofertas_a[len(ofertas_a)-1])
				fu_oferta_ba_t_1 = funcion_utilidad(2,tipo_fu,ofertas_b[len(ofertas_b)-1])
				fu_oferta_ba_t_D = funcion_utilidad(2,tipo_fu,ofertas_b[len(ofertas_b)-D])
				if(D == 1):
					return 1
				else:
					fu_oferta_ba_t_D_1 = funcion_utilidad(2,tipo_fu,ofertas_b[len(ofertas_b)-D+1])
			# tipo: relativo, absoluto, promediado
			if(tipo == "relativo"): 
				s = min(1,max(RU,((1-fu_oferta_ba_t_D_1)/(1-fu_oferta_ba_t_D))*fu_oferta_ab_t_1))
			elif(tipo == "absoluto"):
				s = min(1,max(RU,fu_oferta_ab_t_1-fu_oferta_ba_t_D_1-fu_oferta_ba_t_D))
			else: # tipo = promediado
				s = min(1,max(RU,((1-fu_oferta_ba_t_1)/(1-fu_oferta_ba_t_D))*fu_oferta_ab_t_1))
			return s
		else:
			return 1
	# elif(opcion == 3):
	# elif(opcion == 4):
	# elif(opcion == 5):
	# ...
	return 0