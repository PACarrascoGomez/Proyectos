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
fichero = file("datos_test.dat")
test = pickle.load(fichero)
fichero.close()
fichero = file("lambda.dat")
umbral = pickle.load(fichero)
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

# Size ventana de analisis
l_sr = len(test[0][0])/16

# Evaluacion
vp = 0
vn = 0
fp = 0
fn = 0
total_caras = 0
total_no_caras = 0
for i in range(0,len(test)):
	img = test[i][0]
	clase = test[i][1]
	if clase == 1:
		total_caras += 1
	else:
		total_no_caras += 1
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
	if aux_producto > umbral: # cara
		if clase == 1:
			vp += 1
		else:
			fp += 1
	else:
		if clase == 0:
			vn += 1
		else:
			fn += 1


# Resultados
print "-----------------------------------"
print "\t\tRESULTADOS"
print "-----------------------------------"
print "Verdaderos positivos (VP): ",vp
print "Falsos positivos (FP): ",fp
print "Verdaderos negativos (VN)",vn
print "Falsos negativos (FN)",fn
print "Caras analizadas: ", total_caras
print "No caras analizadas: ", total_no_caras
print "-----------------------------------"

