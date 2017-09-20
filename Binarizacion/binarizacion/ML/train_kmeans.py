import sys
from utils import *
from sklearn.neighbors.nearest_centroid import NearestCentroid
import pickle

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: K-means (Clustering)
# Tecnica: Binarizacion (ML)
# Asignatura: Reconocimiento de escritura
##############################################

# Uso: python3 train_kmeans.py ../../DataSet_Propio/train/X/ ../../DataSet_Propio/train/Y/ 3

# Comprobacion de parametros
if len(sys.argv) != 4:
	print ("Uso: python3 train_kmeans.py <dir_x_train> <dir_y_train> <size_windows>")
	exit()

# Parametros de entrada
dir_x = sys.argv[1]
dir_y = sys.argv[2]

# Dimension de la ventana de analisis
s_w = int(sys.argv[3])

# Obtenemos x_train e y_train
x_train,y_train = load_data(dir_x,dir_y,s_w)

#------------------------------------------
# MODELO
#------------------------------------------
clf = NearestCentroid()

#------------------------------------------
# ENTRENAMIENTO
#------------------------------------------
clf.fit(x_train, y_train)

#------------------------------------------
# Almacenamos el modelo obtenido
#------------------------------------------
f_out = open("model_kmeans","wb")
pickle.dump(clf,f_out)
f_out.close()
