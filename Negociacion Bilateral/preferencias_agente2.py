
###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: Sistemas multiagente (SMA)
# Trabajo: Entorno de negociacion automatica bilateral
# Descripcion: Preferencias del agente 2 en la negociacion
# Dominio: Compra/Venta de portatil
# Lenguaje: python2.7
###########################################################

#---------------------------------------
# Agente vendedor
#---------------------------------------

# Devuelve el vector de pesos
def w_agente2():
	# Definimos los pesos
	return [0.2,0.1,0.1,0.2,0.3,0.1]

# Devuelve el vector de valoraciones para una oferta
def v_agente2(oferta):
	# Definimos vector de valoraciones
	v = [0]*len(w_agente2())
	# Valoracion atributo 1 = RAM (GB)
	if(oferta[0] >= 32):
		v[0] = 0.2
	elif(12 < oferta[0] < 32):
		v[0] = 0.4
	else:
		v[0] = 1
	# Valoracion atributo 2 = HDD (GB)
	if(oferta[1] >= 1000):
		v[1] = 0.2
	elif(500 < oferta[1] < 1000):
		v[1] = 0.6
	else:
		v[1] = 1
	# Valoracion atributo 3 = Pulgadas Monitor (Pulgadas)
	if(oferta[2] >= 15.6):
		v[2] = 0.6
	elif(13.3 < oferta[2] < 15.6):
		v[2] = 1
	else:
		v[2] = 0.2
	# Valoracion atributo 4 = Peso (Kg)
	if(oferta[3] >= 3):
		v[3] = 1
	elif(1 < oferta[3] < 3):
		v[3] = 0.8
	else:
		v[3] = 0.2
	# Valoracion atributo 5 = Precio
	if(oferta[4] >= 1200):
		v[4] = 1
	elif(600.75 < oferta[4] < 1200):
		v[4] = 0.4
	else:
		v[3] = 0.2
	# Valoracion atributo 6 = Color
	if(oferta[5] == "plata"):
		v[5] = 1
	elif(oferta[5] == "azul"):
		v[5] = 0.6
	elif(oferta[5] == "negro"):
		v[5] = 0.4
	else:
		v[5] = 0.1
	# Retornamos el vector de valores
	return v