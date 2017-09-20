import sys
import cPickle as pickle
import numpy as np

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Entorno: python2.7
# Descripcion: Unir datos de la practica con datos adicionales
###########################################################

# Parametros
if len(sys.argv) != 4:
	print "Uso: python2 unir_datos.py <f_practicas> <f_incremental> <nombre_f_salida>"
	sys.exit(1)

# EDA
lista = []

# Cargamos los datos proporcionados para la practica
f = open(sys.argv[1],"r")
texto = f.read()
f.close()
lineas = texto.split("\n")
lineas = lineas[0:len(lineas)-1]
for l in lineas:
	aux = l.split(" ")
	aux = aux[1:len(aux)] # La primera posicion es ''
	img = []
	for a in aux:
		img.append(float(a))
	lista.append(img)

# Cargamos los datos adicionales
f = file(sys.argv[2],"rb")
l_aux = pickle.load(f)
f.close()

# Unimos los datos
lista = lista + l_aux

# Convertimos la EDA a un vector numpy (menor espacio)
m_lista = np.array(lista)

# Almacenamos la matriz
f = file(sys.argv[3],"wb")
pickle.dump(m_lista,f,2)
f.close()
