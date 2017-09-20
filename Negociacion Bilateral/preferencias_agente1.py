
###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: Sistemas multiagente (SMA)
# Trabajo: Entorno de negociacion automatica bilateral
# Descripcion: Preferencias del agente 1 en la negociacion
# Dominio: Compra/Venta de portatil
# Lenguaje: python2.7
###########################################################

#---------------------------------------
# Agente comprador
#---------------------------------------

# Devuelve el vector de pesos
def w_agente1():
	# Definimos los pesos
	return [0.3,0.2,0.2,0.1,0.1,0.1]

# Devuelve el vector de valoraciones para una oferta
def v_agente1(oferta):
	# Definimos vector de valoraciones
	v = [0]*len(w_agente1())
	# Valoracion atributo 1 = RAM (GB)
	if(oferta[0] >= 12):
		v[0] = 1
	elif(6 < oferta[0] < 12):
		v[0] = 0.5
	else:
		v[0] = 0.1
	# Valoracion atributo 2 = HDD (GB)
	if(oferta[1] >= 750):
		v[1] = 1
	elif(240 < oferta[1] < 750):
		v[1] = 0.4
	else:
		v[1] = 0
	# Valoracion atributo 3 = Pulgadas Monitor (Pulgadas)
	if(oferta[2] > 15.6):
		v[2] = 0.2
	elif(13.3 <= oferta[2] <= 15.6):
		v[2] = 1
	else:
		v[2] = 0
	# Valoracion atributo 4 = Peso (Kg)
	if(oferta[3] >= 4):
		v[3] = 0
	elif(2 < oferta[3] < 4):
		v[3] = 0.4
	else:
		v[3] = 1
	# Valoracion atributo 5 = Precio
	if(oferta[4] >= 1000):
		v[4] = 0
	elif(550.50 < oferta[4] < 1000):
		v[4] = 0.4
	else:
		v[3] = 1
	# Valoracion atributo 6 = Color
	if(oferta[5] == "negro"):
		v[5] = 1
	elif(oferta[5] == "azul"):
		v[5] = 0.6
	else:
		v[5] = 0
	# Retornamos el vector de valores
	return v