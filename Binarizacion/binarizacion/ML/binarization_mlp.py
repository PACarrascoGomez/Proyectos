import sys
import cv2
from utils import *
import numpy as np
from keras.models import load_model
import pickle

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: MLP
# Tecnica: Binarizacion (ML)
# Asignatura: Reconocimiento de escritura
##############################################

# Uso: python3 binarization_mlp.py ../../DataSet_Propio/test/X/i4.jpg model_mlp.h5 salida.jpg 3

# Comprobacion de parametros
if len(sys.argv) != 5:
	print ("Uso: python3 binarization_mlp.py <image> <model> <image_out> <size_windows>")
	exit()

# Parametros de entrada
f_img_in = sys.argv[1]
f_model = sys.argv[2]
f_img_out = sys.argv[3]

# Dimension de la ventana de analisis
s_w = int(sys.argv[4])

# Obtenemos x
#x = load_x(f_img_in,s_w)
x = load_x(f_img_in,s_w)

#------------------------------------------
# MODELO
#------------------------------------------
# Cargamos el modelo
model = load_model(f_model)

#------------------------------------------
# PREDICCION
#------------------------------------------
y = model.predict_classes(x,batch_size=128)
y = y.tolist()

#------------------------------------------
# IMAGEN BINARIZADA
#------------------------------------------
binarize_image(f_img_in,f_img_out,y)
