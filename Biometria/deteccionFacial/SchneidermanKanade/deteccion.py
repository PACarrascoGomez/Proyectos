import sys, os
import numpy as np
import cv2
from sklearn.decomposition import IncrementalPCA
from sklearn.cluster import MiniBatchKMeans
import cPickle as pickle
import math

############################################
# Autor: Pascual Andres Carrasco Gomez
# Entorno: python2.7
# Descripcion: Deteccion facial
#	Algoritmo Schneiderman and Kanade
# Nota: El programa requiere:
#	apt-get install python-pip
#	pip install -U scikit-learn
#	pip install -U scipy
#	apt-get install python-opencv
############################################

#-------------------------------------------
# Parametros
#-------------------------------------------
if len(sys.argv) != 5:
	print("Uso: python2 deteccion.py <image> <size_window> <scale> <stride>")
	sys.exit(1)

def imagen_integral(img):
	img_integral = np.zeros((len(img),len(img[0])),dtype=int)
	img_integral[0][0] = img[0][0]
	for r in range(1,len(img)): # 1 Fila
		img_integral[r][0] = img_integral[r-1][0]+img[r][0]
	for c in range(1,len(img[0])): # 1 Columna
		img_integral[0][c] = img_integral[0][c-1]+img[0][c]
	for r in range(1,len(img)): # Resto de matriz
		aux_sum = img[r][0]
		for c in range(1,len(img[0])):
			aux_valor = aux_sum+img[r][c]
			img_integral[r][c] = img_integral[r-1][c]+aux_valor
			aux_sum = aux_valor
	return img_integral


def encuadrar_cara(img,r,c,size):
	for i in range(0,size):
		if r+size < len(img) and c+size < len(img[0]):
			img[r+i,c-1] = (255,0,0)
			img[r+i,c+size] = (255,0,0)
			img[r-1,c+i] = (255,0,0)
			img[r+size,c+i] = (255,0,0)


# Cargar los parametros
fichero = file("pca.dat")
pca = pickle.load(fichero)
fichero.close()
fichero = file("kmeans.dat")
kmeans = pickle.load(fichero)
fichero.close()
fichero = file("q_caras.dat")
q_caras = pickle.load(fichero)
fichero.close()
fichero = file("q_no_caras.dat")
q_no_caras = pickle.load(fichero)
fichero.close()
fichero = file("m_pos_q_caras.dat")
m_pos_q_caras = pickle.load(fichero)
fichero.close()
fichero = file("lambda.dat")
umbral = pickle.load(fichero)
fichero.close()

# Cargamos la imagen en escala de grises
img = cv2.imread(sys.argv[1],0)
img_or = cv2.imread(sys.argv[1],1)

# Variables
n_X = []
# Ventana de analisis (cuadrada)
l_w = int(sys.argv[2])
# Ventana subregion (cuadrada)
l_sr = l_w/4
# stride
pad = int(sys.argv[4])

q_escala = 0
escala = float(sys.argv[3])
# Imagen con diferentes resoluciones
while(len(img) > l_w and len(img[0]) > l_w):
	# Dimensiones de la imagen
	rows = len(img)
	cols = len(img[0])

	# Prepoceso
	for r in range(0,rows,pad):
		for c in range(0,cols,pad):
			if r+l_w <= rows and c+l_w <= cols:
				aux_region = img[r:r+l_w, c:c+l_w]
				x = np.mean(aux_region)
				o = np.std(aux_region)
				if x != 0.0 and o != 0.0:
					region = np.zeros((len(aux_region),len(aux_region[0])),dtype=float)
					for i in range(0,len(region)):
						for j in range(0,len(region[0])):
							region[i][j] = (aux_region[i][j]-x)/o
					#cv2.imshow('image',region)
					#cv2.waitKey(0)
					# Dividimos la region en subregiones
					labels = []
					for r_g in range(0,l_w,l_sr):
						for c_g in range(0,l_w,l_sr):
							if r_g+l_sr <= l_w and c_g+l_sr <= l_w:
								sub_region = region[r_g:r_g+l_sr, c_g:c_g+l_sr]
								l_sub_region = sub_region.tolist()
								aux = []
								for i in range(0,len(l_sub_region)):
									aux = aux + l_sub_region[i]
								aux2 = np.array([aux])
								#n_X.append(pca.transform(aux2)[0])
								X = pca.transform(aux2)[0]
								label = kmeans.predict([X])
								labels.append(label[0])
					aux_producto = 1
					for i in range(0,len(labels)):
						p_p_q_cara = m_pos_q_caras[i][labels[i]]
						p_q_cara = q_caras[labels[i]]
						p_q_no_cara = q_no_caras[labels[i]]
						aux = (p_p_q_cara*p_q_cara)/(p_q_no_cara/16.0)
						aux_producto = aux_producto * aux
					if aux_producto > umbral:
						#cv2.imshow('image',aux_region)
						#cv2.waitKey(0)
						encuadrar_cara(img_or,int(r/math.pow(escala,q_escala)),int(c/math.pow(escala,q_escala)),int(l_w/math.pow(escala,q_escala)))

	# Redimensionamos la imagen
	aux_img = img[:]
	img = cv2.resize(aux_img,(0,0),fx=escala,fy=escala)
	q_escala += 1


# Mostramos la deteccion sobre la imagen original
cv2.imshow('image',img_or)
cv2.waitKey(0)
