import sys
import cv2
from utils import *
import numpy as np
import pickle

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodos:
#	- SVM
#	- K-means
#	- K-neighbors
# Tecnica: Binarizacion (ML)
# Asignatura: Reconocimiento de escritura
##############################################

# Uso: python3 binarization.py ../../DataSet_Propio/test/X/i4.jpg model_kmeans salida.jpg 3

# Comprobacion de parametros
if len(sys.argv) != 5:
	print ("Uso: python3 binarization.py <image> <model> <image_out> <size_windows>")
	exit()

# Parametros de entrada
f_img_in = sys.argv[1]
f_model = sys.argv[2]
f_img_out = sys.argv[3]

# Dimension de la ventana de analisis
s_w = int(sys.argv[4])

# Obtenemos x
x = load_x(f_img_in,s_w)

#------------------------------------------
# MODELO
#------------------------------------------
# Cargamos el modelo
f = open(f_model,"rb")
clf = pickle.load(f)
f.close()

#------------------------------------------
# PREDICCION
#------------------------------------------
y = clf.predict(x)
y = y.tolist()

#------------------------------------------
# IMAGEN BINARIZADA
#------------------------------------------
binarize_image(f_img_in,f_img_out,y)
