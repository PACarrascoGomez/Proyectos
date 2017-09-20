from random import randint as rand
import numpy as np
import cv2
import sys, os
import cPickle as pickle

############################################
# Autor: Pascual Andres Carrasco Gomez
# Entorno: python2.7
# Descripcion: crop imagenes para no caras
############################################

# Comprobamos parametros
if len(sys.argv) != 5:
	print "Uso: python2.7 crop_imagen.py <dir_imagenes> <size_crop> <n_crops> <nombre_f_salida>"
	sys.exit(1)

# EDA
l_imagenes_no_caras = []

# Parametros
n_muestras = int(sys.argv[3])
size_w = int(sys.argv[2])

# Cargamos las imagenes de donde obtenemos los crop de no caras
lista_imagenes = os.popen("ls " + sys.argv[1]).read().split("\n")
lista_imagenes = lista_imagenes[0:len(lista_imagenes)-1]
n_muestras_x_imagen = n_muestras/len(lista_imagenes)

# Obtenemos los crops de la imagen de forma aleatoria
generados = 0
for i in range(0,len(lista_imagenes)):
	img = cv2.imread(sys.argv[1]+lista_imagenes[i],0)
	rows = len(img)
	cols = len(img[0])
	l_puntos = []
	cont = 0
	while cont < n_muestras_x_imagen:
		x = rand(0,rows)
		y = rand(0,cols)
		while (x,y) in l_puntos or (x+size_w >= rows or y+size_w >= cols):
			x = rand(0,rows)
			y = rand(0,cols)
		l_puntos.append((x,y))
		crop = img[x:x+size_w, y:y+size_w]
		# Normalizamos
		x = np.mean(crop)
		o = np.std(crop)
		if x != 0.0 and o != 0.0:
			crop_norm = np.zeros((len(crop),len(crop[0])),dtype=float)
			for i in range(0,len(crop_norm)):
				for j in range(0,len(crop_norm[0])):
					crop_norm[i][j] = (crop[i][j]-x)/o
			# Actualizamos la lista
			img_aux = np.reshape(crop_norm,(1,size_w*size_w))
			l_aux_img = img_aux.tolist()[0]
			l_imagenes_no_caras.append(l_aux_img)
			cont += 1	

# Almacenamos las nuevas imagenes
f = file(sys.argv[4],"wb")
pickle.dump(l_imagenes_no_caras,f,2)
f.close()

