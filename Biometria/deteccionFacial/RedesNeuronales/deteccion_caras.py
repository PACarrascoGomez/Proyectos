from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import cv2
import sys, os
import numpy as np
import math
from keras.models import load_model

######################################################
# Autor: Pascual Andres Carrasco Gomez
# 
# Requerimientos:
#	apt-get install python-numpy python-scipy python-dev python-pip python-nose g++ libopenblas-dev git
#	pip install Theano
#	pip install keras
######################################################

# Parametros
if len(sys.argv) != 5:
	print "Uso: python2 deteccion_caras.py <image> <modelo> <size_window> <size_stride>"
	sys.exit(1)

def encuadrar_cara(img,r,c,size):
	for i in range(0,size):
		if r+size < len(img) and c+size < len(img[0]):
			img[r+i,c-1] = (255,0,0)
			img[r+i,c+size] = (255,0,0)
			img[r-1,c+i] = (255,0,0)
			img[r+size,c+i] = (255,0,0)

# Cargamos el modelo
model = load_model(sys.argv[2])

# Cargamos la imagen de entrada
img = cv2.imread(sys.argv[1],0)
img_or = cv2.imread(sys.argv[1],1)

# Tamano de la ventana de analisis
size_w = int(sys.argv[3])

# Stride
pad = int(sys.argv[4])

q_escala = 0
escala = 0.9
while len(img) > size_w and len(img[0]) > size_w:

	x_aux = []
	rows = len(img)
	cols = len(img[0])
	for r in range(0,rows,pad):
		for c in range(0,cols,pad):
			if r+size_w < rows and c+size_w < cols:
				aux_region = img[r:r+size_w,c:c+size_w]
				x = np.mean(aux_region)
				o = np.std(aux_region)
				region = np.zeros((len(aux_region),len(aux_region[0])),dtype=float)
				for i in range(0,len(region)):
					for j in range(0,len(region[0])):
						region[i][j] = (aux_region[i][j]-x)/o
				region = np.reshape(region,(1,len(region)*len(region[0])))
				clase = model.predict_classes(region,batch_size=25)
				if clase == 1: # Cara detectada
					encuadrar_cara(img_or,int(r/math.pow(escala,q_escala)),int(c/math.pow(escala,q_escala)),int(size_w/math.pow(escala,q_escala)))

	# Reducimos la imagen segun el factor de escala
	aux_img = img[:]
	img = cv2.resize(aux_img,None,fx=0.9,fy=0.9,interpolation=cv2.INTER_CUBIC)
	q_escala += 1
			
cv2.imshow('image',img_or)
cv2.waitKey(0)
