import sys
from utils import *
from sklearn.neighbors import KNeighborsClassifier
import pickle

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: K-vecinos mas cercanos
# Tecnica: Binarizacion (ML)
# Asignatura: Reconocimiento de escritura
##############################################

# Uso: python3 train_kneighbours.py ../../DataSet_Propio/train/X/ ../../DataSet_Propio/train/Y/ 3 2

# Comprobacion de parametros
if len(sys.argv) != 5:
	print ("Uso: python3 train_kneighbours.py <dir_x_train> <dir_y_train> <size_windows> <k_neighbours>")
	exit()

# Parametros de entrada
dir_x = sys.argv[1]
dir_y = sys.argv[2]

# Dimension de la ventana de analisis
s_w = int(sys.argv[3])

# K vecinos mas cercanos
k = int(sys.argv[4])

# Obtenemos x_train e y_train
x_train,y_train = load_data(dir_x,dir_y,s_w)

#------------------------------------------
# MODELO
#------------------------------------------
neigh = KNeighborsClassifier(n_neighbors=k)

#------------------------------------------
# ENTRENAMIENTO
#------------------------------------------
neigh.fit(x_train,y_train)

#------------------------------------------
# Almacenamos el modelo obtenido
#------------------------------------------
f_out = open("model_kneighbours","wb")
pickle.dump(neigh,f_out)
f_out.close()
