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


# Cargar los parametros
fichero = file("datos_dev.dat")
dev = pickle.load(fichero)
fichero.close()
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

l_sr = len(dev[0][0])/16

suma_caras = 0.0
n_caras = 0
suma_no_caras = 0.0
n_no_caras = 0
for i in range(0,len(dev)):
	img = dev[i][0]
	clase = dev[i][1]
	labels = []
	for i in range(0,len(img),l_sr):
		if i+l_sr <= len(img):
			subregion = img[i:i+l_sr]
			X = pca.transform([subregion])[0]
			label = kmeans.predict([X])
			labels.append(label[0])
	aux_producto = 1
	for i in range(0,len(labels)):
		p_p_q_cara = m_pos_q_caras[i][labels[i]]
		p_q_cara = q_caras[labels[i]]
		p_q_no_cara = q_no_caras[labels[i]]
		aux = (p_p_q_cara*p_q_cara)/(p_q_no_cara/16.0)
		aux_producto = aux_producto * aux
	if clase == 1: # cara
		suma_caras += aux_producto
		n_caras += 1
	else: # no cara
		suma_no_caras += aux_producto
		n_no_caras += 1

umbral = (suma_no_caras/n_no_caras)/(suma_caras/n_caras)
print "Umbral: ",umbral

# Almacenamos el valor de lambda
fichero = file("lambda.dat", "w")  
pickle.dump(umbral, fichero, 2) # 2 = Almacenamiento binario
fichero.close()  